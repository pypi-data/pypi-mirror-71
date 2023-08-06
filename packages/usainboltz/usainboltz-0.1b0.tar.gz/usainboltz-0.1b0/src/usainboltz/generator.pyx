# coding: utf-8

# cython: profile=True

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""Boltzmann generator for Context-free grammars.

This module provides functions for generating combinatorial objects (i.e.
objects described by a combinatorial specification, see
:mod:`usainboltz.grammar`) according to the Boltzmann
distribution.

Given an unlabelled combinatorial class A, the Boltzmann distribution of
parameter :math:`x` is such that an object of size n is drawn with the
probability :math:`\frac{x^n}{A(x)}` where :math:`A(x)` denotes the ordinary
generating function of A.  For labelled classes, this probability is set to
:math:`\frac{x^n}{n!A(x)}` where :math:`A(x)` denotes the exponential
generating function of A. See [DuFlLoSc04]_ for details.

By default, the objects produced by the generator are nested tuples of strings
(the atoms). For instance ``('z', ('z', 'epsilon', 'epsilon'), ('z', 'epsilon', 'epsilon'))`` is a
balanced binary tree with 3 internal nodes (z) and 4 leaves (e). To alter this
behaviour and generate other types of objects, you can specify a builder
function for each type of symbol in the grammar. The behaviour of the builders
is that they are applied in bottom up order to the structure "on the fly" during
generation. For instance, in order to generate Dyck words using the grammar for
binary trees, one can use a builder that return ``""`` for each leaf ``"(" +
left child + ")" + right child`` for each node. The builders will receive a
tuple for each product, a string for each atom and builders for unions should be
computed using the :func:`union_builder` helper. See the example below for the
case of Dyck words.

Examples:
    >>> from usainboltz import *

    Both binary trees and Dyck words can be generated from the following
    grammar

    >>> epsilon, z, B = Epsilon(), Atom(), RuleName("B")
    >>> grammar = Grammar({B: epsilon + z * B * B})
    >>> generator = Generator(grammar, B, singular=True)

    In order to build Dyck words, one can interpret epsilon as the empty word
    and nodes as the derivation: ``D -> ( D ) D``

    >>> def leaf_builder(_):
    ...     return ""

    >>> def node_builder(tuple):
    ...     _, left, right = tuple
    ...     return "(" + left + ")" + right

    >>> generator.set_builder(B, union_builder(leaf_builder, node_builder))
    >>> dyck_word = generator.sample((10, 20))
    >>> dyck_word  # random
    '((())(())())()()(())'
    >>> len(dyck_word) in range(20, 41)
    True

    If on the contrary we want to see trees as S-expressions, we can interpret
    epsilon as the leaf ``"leaf"`` and nodes as ``(node left_child
    right_child)``

    >>> def leaf_builder(_):
    ...     return "leaf"

    >>> def node_builder(tuple):
    ...     _, left, right = tuple
    ...     return "(node {} {})".format(left, right)

    >>> generator.set_builder(B, union_builder(leaf_builder, node_builder))
    >>> print(generator.sample((10, 20)))
    (node
      (node
        (node
          (node
            (node
              (node leaf leaf)
              (node
                leaf
                (node
                  (node leaf leaf)
                  (node
                    (node
                      (node
                        leaf
                        (node leaf leaf))
                      (node (node leaf leaf) (node leaf leaf)))
                    leaf))))
            leaf)
          (node leaf leaf))
        leaf)
      (node
        (node leaf leaf)
        (node leaf leaf)))

    Note that the builders mechanism can also be used to compute some
    statistics on the fly without explicitly building the whole structure. For
    instance the following example illustrates how to generate the **height**
    of a tree following the Boltzmann distribution without building the tree.

    >>> def leaf_height(_):
    ...     return 0

    >>> def node_height(tuple):
    ...     _, left, right = tuple
    ...     return 1 + max(left, right)

    >>> generator.set_builder(B, union_builder(leaf_height, node_height))
    >>> height = generator.sample((10, 20))
    >>> height  # random
    7

For labelled grammar, the procedure is the same. In this case, the default
builders also output the labelling, they do not only generate the structure.

Example:
    >>> z = Atom()
    >>> e, M = Epsilon(), RuleName()
    >>> g = Grammar({M: e + z * M + z * M * M}, labelled=True)
    >>> generator = Generator(g, M, singular=True)
    >>> generator.sample((5,10))  # random
    (2, (1, (4, (3, (5, 'epsilon'), 'epsilon'))), 'epsilon')

"""

import copy
from functools import reduce

from usainboltz.grammar import (
    Atom,
    Cycle,
    Epsilon,
    Marker,
    MSet,
    Product,
    RuleName,
    Seq,
    Set,
    Union,
    UCycle,
)
from usainboltz.oracle import build_oracle

from xoshiro cimport xoshiro
from libc.math cimport log, ceil, exp
from libc.stdint cimport uint64_t

cpdef seed(s):
    xoshiro.seed(s)

ctypedef enum instruction:
    # Symbols
    REF,
    ATOM,
    MARKER,
    EPSILON,
    # Grammar combinators
    UNION,
    PRODUCT,
    SEQ,
    SET,
    MSET,
    # Special instructions used by the random generators
    TUPLE,
    LIST,
    SET_PRODUCT,
    FUNCTION,
    WRAP_CHOICE,
    WRAPPED_CHOICE

# ------------------------------------------------------- #
# Grammar preprocessing
# ------------------------------------------------------- #

# For performance reasons, we use integers rather that strings to identify
# symbols during generation and we drop the python classes in favour of nested
# tuples. The following functions implement this transformation.
#
# All of this should remain hidden from the end user.

class Mapping:
    def __init__(self, grammar):
        # Rule names
        rule_name_to_id, id_to_rule_name = self._make_mapping(grammar.rules.keys())
        self.rule_name_to_id = rule_name_to_id
        self.id_to_rule_name = [id_to_rule_name[i] for i in range(len(id_to_rule_name))]
        # Markers
        marker_to_id, id_to_marker = self._make_mapping(grammar.markers())
        self.marker_to_id = marker_to_id
        self.id_to_marker = [id_to_marker[i] for i in range(len(id_to_marker))]

    def nb_rules(self):
        return len(self.id_to_rule_name)

    def nb_markers(self):
        return len(self.id_to_marker)

    @staticmethod
    def _make_mapping(iterable, start=0):
        x_to_id = {}
        id_to_x = {}
        for i, x in enumerate(iterable, start=start):
            x_to_id[x] = i
            id_to_x[i] = x
        return x_to_id, id_to_x

cdef float factorial(int n):
    cdef float res = 1.
    for i in range(2, n + 1):
        res *= float(i)
    return res


cdef _map_all_names_to_ids_expr(mapping, weights, expr):
    """Recursively transform an expression into a tuple of the form
    (RULE_TYPE, weight, args) where:
    - RULE_TYPE encodes the type of the expression [ATOM|REF|PRODUCT|...]
    - weight is the value of the generating function of this expression
    - args is auxilliary information (the name of an atom, the components of an
      union, ...)
    """
    # Symbols
    if isinstance(expr, RuleName):
        return (REF, weights[expr], mapping.rule_name_to_id[expr])
    elif isinstance(expr, Atom):
        return (ATOM, weights[expr], None)
    elif isinstance(expr, Marker):
        return (MARKER, weights[expr], (mapping.marker_to_id[expr], expr.name))
    elif isinstance(expr, Epsilon):
        return (EPSILON, 1., None)
    # Grammar combinators
    elif isinstance(expr, Union):
        args = tuple((_map_all_names_to_ids_expr(mapping, weights, arg) for arg in expr.args))
        total_weight = sum([w for (__, w, __) in args])
        return (UNION, total_weight, args)
    elif isinstance(expr, Product):
        args = tuple((_map_all_names_to_ids_expr(mapping, weights, arg) for arg in expr.args))
        total_weight = reduce(
            lambda x, y: x * y,
            [w for (__, w, __) in args],
            1.
        )
        return (PRODUCT, total_weight, args)
    elif isinstance(expr, Seq):
        rule = _map_all_names_to_ids_expr(mapping, weights, expr.arg)
        _, arg_weight, _ = rule
        full_series = 1. / (1. - arg_weight)
        weight = full_series
        if expr.lower_size is not None:
            weight *= arg_weight ** expr.lower_size
        if expr.upper_size is not None:
            weight -= arg_weight ** expr.upper_size * full_series
        return (SEQ, weight, (rule, expr.lower_size, expr.upper_size))
    elif isinstance(expr, Set):
        rule = _map_all_names_to_ids_expr(mapping, weights, expr.arg)
        _, arg_weight, _ = rule
        lower_size = expr.lower_size if expr.lower_size is not None else 0
        if expr.upper_size is not None:
            weight = sum(
                arg_weight ** i / factorial(i)
                for i in range(lower_size, expr.upper_size + 1)
            )
        else:
            weight = exp(arg_weight)
            weight -= sum(
                arg_weight ** i / factorial(i)
                for i in range(lower_size)
            )
        return (SET, weight, (rule, expr.lower_size, expr.upper_size))
    elif isinstance(expr, MSet):
        if expr.lower_size is not None or expr.upper_size is not None:
            raise NotImplementedError("Generator: size constraints on MSet")
        rule = _map_all_names_to_ids_expr(mapping, weights, expr.arg)
        weight = 0.  # this info should come from the oracle
        a_values = []  # this info shoud come from the oracle
        raise NotImplementedError("Generator: MSet weight")
        #  (MSET, weight, (rule, a_values))
    elif isinstance(expr, Cycle):
        raise NotImplementedError("Generator: Cycle")
    elif isinstance(expr, UCycle):
        raise NotImplementedError("Generator: UCycle")
    else:
        raise NotImplementedError("_map_all_names_to_ids({})".format(type(expr)))

cdef _map_all_names_to_ids_system(mapping, weights, rules):
    return [
        _map_all_names_to_ids_expr(mapping, weights, rules[mapping.id_to_rule_name[i]])
        for i in range(mapping.nb_rules())
    ]


# ------------------------------------------------------- #
# Generic builders
# ------------------------------------------------------- #

# When it chooses one possible derivation for a union rule, the random
# generator wraps the generated object in a tuple of the form ``(choice_id,
# object)`` so that the builder that will be called on this value has the
# information of which derivation was chosen. This helper function hides this
# machinery to the end user, allowing her to compose builders in a "high-level"
# manner.

def union_builder(*builders):
    """Factory for generating builders for union rules.

    The recommended way to write a builder for a union rule is to use this
    helper: write a auxilliary builder for each component of the union and
    compose them with ``union_builder``.

    Args:
        builders (List[function]): builder functions, one for each component of
            the union.

    Returns:
        function: a builder function for a disjoint union. The resulting
            function applies one of the functions passed as arguments to its
            input depending of the component of the union its argument belongs
            to.

    Examples:
        Assume the symbol ``D`` is defined by ``Union(A, B, C)``, then
        defining a builder for D looks like:

        >>> def build_A(args):
        ...     # Do something
        ...     pass

        >>> def build_B(args):
        ...     # Do something
        ...     pass

        >>> def build_C(args):
        ...     # Do something
        ...     pass

        >>> build_D = union_builder(build_A, build_B, build_C)

        For instance, for binary trees defined by ``B = Union(leaf, Product(z,
        B, B))``, this could be:

        >>> def build_leaf(_):
        ...     return BinaryTree()

        >>> def build_node(args):
        ...     z, left, right = args
        ...     return BinaryTree([left, right])

        >>> build_binarytree = union_builder(build_leaf, build_node)

    """
    def build(obj):
        index, content = obj
        builder = builders[index]
        return builder(content)
    return build

# The following functions generate the default builders for labelled and
# unlabelled structures. These builders produce nested tuples. Choices ids are
# omitted for readability.

cdef inline identity(x):
    return x

cdef inline ProductBuilder(builders):
    def build(terms):
        return tuple(builders[i](terms[i]) for i in range(len(terms)))
    return build

cdef inline SeqBuilder(builder):
    def build(terms):
        return [builder(term) for term in terms]
    return build

cdef make_default_builder(rule):
    """Generate the default builders for a rule.

    Args:
        rule (Rule): a grammar rule.

    Returns:
        function: a simple builder for the rule passed as argument that
            generate objects as nested tuples.
    """
    # Symbols
    if isinstance(rule, RuleName):
        return identity
    elif isinstance(rule, (Atom, Marker, Epsilon)):
        return identity
    # Grammar combinators
    elif isinstance(rule, Product):
        subbuilders = [make_default_builder(component) for component in rule.args]
        return ProductBuilder(subbuilders)
    elif isinstance(rule, Seq):
        subbuilder = make_default_builder(rule.arg)
        return SeqBuilder(subbuilder)
    elif isinstance(rule, Set):
        subbuilder = make_default_builder(rule.arg)
        # Same as Seq
        return SeqBuilder(subbuilder)
    elif isinstance(rule, Union):
        subbuilders = [make_default_builder(component) for component in rule.args]
        return union_builder(*subbuilders)
    else:
        raise NotImplementedError("make_default_builder({})".format(type(rule)))


# ------------------------------------------------------- #
# Random generation
# ------------------------------------------------------- #

cpdef int bounded_geometric(double param, lower_bound, upper_bound):
    cdef double r = xoshiro.rand_double()

    if lower_bound is None:
        lower_bound = 0

    bounding_term = 0
    if upper_bound is not None:
      k = upper_bound - lower_bound
      bounding_term = (1 - r) * (param ** (k + 1))

    geom = int(ceil(log(r + bounding_term)/log(param) - 1))
    return geom + lower_bound

cpdef int bounded_poisson(
        double total_weight,
        double param,
        lower_bound,
        upper_bound,
    ):
    cdef double r = xoshiro.rand_double() * total_weight
    cdef int i = lower_bound or 0
    cdef double s = 0.

    while s < r:
        s += param ** i / factorial(i)
        i += 1

    if upper_bound is not None:
        assert i <= upper_bound
    return (i - 1)

cpdef int mset_max_index(double total_weight, a_values):
    cdef double r = xoshiro.rand_double() * total_weight
    cdef double cumul = exp(a_values[0])
    cdef int j = 1

    while cumul < r:
        j += 1
        cumul *= exp(a_values[j] / j)

    return j


cdef _rand_perm(unsigned int n):
    """Draw an uniform random premutation of size ``n`` using the Fisher-Yates algorithm."""
    cdef unsigned int i, j
    cdef list p = list(range(1,n+1))

    for i in range(n-1,0,-1):
        j = xoshiro.rand_i64(i)
        p[i], p[j] = p[j], p[i]

    return p

# A free Boltzmann generator, but instead of generating a tree it only computes
# its sizes with respect to each of its atoms.

cdef c_simulate(first_rule, max_sizes, flat_rules):
    cdef sizes = [0 for _ in max_sizes]
    cdef list todo = [first_rule]
    cdef double r = 0.

    cdef instruction type
    cdef double weight

    while todo:
        type, weight, args = todo.pop()
        # Symbols
        if type == REF:
            symbol = args
            todo.append(flat_rules[symbol])
        elif type == ATOM:
            sizes[0] += 1
            if max_sizes[0] is not None and sizes[0] > max_sizes[0]:
                return sizes
        elif type == MARKER:
            symbol_id, _ = args
            symbol_id += 1
            sizes[symbol_id] += 1
            if max_sizes[symbol_id] is not None and sizes[symbol_id] > max_sizes[symbol_id]:
                return sizes
        elif type == EPSILON:
            pass
        # Grammar combinators
        elif type == UNION:
            r = xoshiro.rand_double() * weight
            for arg in args:
                __, arg_weight, __ = arg
                r -= arg_weight
                if r <= 0:
                    todo.append(arg)
                    break
        elif type == PRODUCT:
            todo += args[::-1]
        elif type == SEQ:
            arg, lower_size, upper_size = args
            _, arg_weight, _ = arg
            k = bounded_geometric(arg_weight, lower_size, upper_size)
            for __ in range(k):
                todo.append(arg)
        elif type == SET:
            arg, lower_size, upper_size = args
            _, arg_weight, _ = arg
            k = bounded_poisson(weight, arg_weight, lower_size, upper_size)
            for _ in range(k):
                todo.append(arg)
        elif type == MSET:
            arg, a_values = args
            k0 = mset_max_index(weight, a_values)
            for j in range(1, k0):
                param = a_values[j] / j
                n = bounded_poisson(exp(param), param, None, None)
                for _ in range(n):
                    # Generate j copies of Boltzmann(arg, z^j)
                    pass
            param = a_values[k0] / k0
            n = bounded_poisson(exp(param), param, 1, None)
            for _ in range(n):
                # Generate k0 copies of Boltzmann(arg, z^k0)
                pass
        else:
            raise NotImplementedError("c_simulate({})".format(type))
    return sizes

# Free Boltzmann sampler (actual generation) of *unlabelled* structures.
# Does not handle the labelling of labelled structures

cdef c_generate(first_rule, rules, builders, labels=None):
    cdef list generated = []
    cdef list todo = [first_rule]
    cdef double r = 0.

    while todo:
        type, weight, args = todo.pop()
        # Symbols
        if type == REF:
            symbol = args
            todo.append((FUNCTION, weight, symbol))
            todo.append(rules[symbol])

        elif type == ATOM:
            if labels is not None:
                generated.append(labels.pop())
            else:
                generated.append("z")
        elif type == EPSILON:
            generated.append("epsilon")
        elif type == MARKER:
            _, symbol_name = args
            generated.append(symbol_name)
        # Grammar combinators
        elif type == UNION:
            r = xoshiro.rand_double() * weight
            for i in range(len(args)):
                arg = args[i]
                __, arg_weight, __ = arg
                r -= arg_weight
                if r <= 0:
                    todo.append((WRAP_CHOICE, arg_weight, i))
                    todo.append(arg)
                    break
        elif type == PRODUCT:
            nargs = len(args)
            todo.append((TUPLE, weight, nargs))
            todo += args[::-1]
        elif type == SEQ:
            arg, lower_size, upper_size = args
            _, arg_weight, _ = arg
            k = bounded_geometric(arg_weight, lower_size, upper_size)
            todo.append((LIST, weight, k))
            for __ in range(k):
                todo.append(arg)
        elif type == SET:
            arg, lower_size, upper_size = args
            _, arg_weight, _ = arg
            k = bounded_poisson(weight, arg_weight, lower_size, upper_size)
            # store sets as lists
            todo.append((LIST, weight, k))
            for _ in range(k):
                todo.append(arg)
        # Internal instructions
        elif type == TUPLE:
            nargs = args
            t = tuple(generated[-nargs:])
            generated = generated[:-nargs]
            generated.append(t)
        elif type == LIST:
            nargs = args
            if nargs == 0:
                generated.append([])
            else:
                t = list(generated[-nargs:])
                generated = generated[:-nargs]
                generated.append(t)
        elif type == FUNCTION:
            func = builders[args]
            x = generated.pop()
            generated.append(func(x))
        elif type == WRAP_CHOICE:
            choice = generated.pop()
            choice_number = args
            generated.append((choice_number, choice))
        else:
            raise NotImplementedError("c_generate({})".format(type))

    obj, = generated
    return obj


# ------------------------------------------------------- #
# High level interface
# ------------------------------------------------------- #

cdef _in_sizes_windows(sizes, sizes_windows):
    for i, (size_min, size_max) in enumerate(sizes_windows):
        size = sizes[i]
        if size_min is not None and size < size_min:
            return False
        if size_max is not None and size > size_max:
            return False
    return True

cdef c_gen(first_rule, rules, sizes_windows, builders, labelling=False):
    """Search for a tree in a given size window."""
    cdef max_sizes = [size_max for (_, size_max) in sizes_windows]

    cdef uint64_t[4] backup_state

    # I'd need a do while
    xoshiro.get_state(backup_state)
    cdef sizes = c_simulate(first_rule, max_sizes, rules)
    while not _in_sizes_windows(sizes, sizes_windows):
        # save the random generator's state
        xoshiro.get_state(backup_state)
        sizes = c_simulate(first_rule, max_sizes, rules)

    labels = None
    if labelling:
        n = sizes[0]
        labels = _rand_perm(n)

    # Reset the random generator to the state it was just before the simulation
    xoshiro.set_state(backup_state)

    return c_generate(first_rule, rules, builders, labels=labels)

class GeneratorConfigError(Exception):
    pass

class Generator:
    """High level interface for Boltzmann samplers."""

    def __init__(
        self,
        grammar,
        rule_name=None,
        singular=None,
        expectations=None,
        oracle=None
    ):
        """Make a Generator out of a grammar.

        Args:
            grammar (Grammar): a combinatorial grammar

            rule_name (RuleName): the rule name of the symbol to generate.

            singular (bool): if set, do singular sampling (use the
                singularity of the generating functions as parameter).

            expectations (Dict[Symbol,number]): this is passed to the oracle to
                skew the distribution in order to target some specific values
                for the expected number of the specified symbols. See
                :py:meth:`OracleFromPaganini.tuning` for more details.

            oracle (Oracle): an oracle for computing the values of some
                generating functions. If not supplied, a default generic oracle
                that should work for most use-cases is automatically generated.

        Examples:

        >>> from usainboltz import *

        Some examples using the grammar for binary trees
        >>> z, B = Atom(), RuleName()
        >>> grammar = Grammar({B: Epsilon() + z * B * B})

        Typical use:
        >>> generator = Generator(grammar, B, singular=True)

        Since their is only one symbol in the grammar, the second argument can be
        omitted:
        >>> generator = Generator(grammar, singular=True)

        """
        self.grammar = copy.deepcopy(grammar)
        self.rule_name = self._guess_rule_name(rule_name)
        # Map all symbols in the grammar to an integer identifier.
        # Use arrays rather than dictionaries.
        self.mapping = Mapping(grammar)

        # If `singular` and the expectations are unspecified, do singular sampling
        # by default.
        if singular is None:
            singular = not(bool(expectations))

        # Set up the oracle.
        oracle = oracle or build_oracle(grammar)
        self.oracle_values = oracle.tuning(
            rule=Atom() if singular else rule_name,
            expectations=expectations,
            singular=singular
        )

        # Initialise the default builders.
        self.builders = [
            make_default_builder(self.grammar.rules[self.mapping.id_to_rule_name[id]])
            for id in range(self.mapping.nb_rules())
        ]

        # Convert the grammar into an array of tuples (for performance)
        self.flat_rules = _map_all_names_to_ids_system(
            self.mapping,
            self.oracle_values,
            self.grammar.rules
        )

    def _guess_rule_name(self, rule_name):
        if rule_name is not None:
            return rule_name
        rule_names = self.grammar.rules.keys()
        if len(rule_names) == 1:
            (rule_name, ) = rule_names
            return rule_name
        raise GeneratorConfigError(
            "I cannot guess which rule you want to generate. "
            "Specify a rule name using ``Generator(rule_name=...)``."
        )

    def _sanitize_windows(self, sizes_windows):
        if sizes_windows is None:
            sizes_windows = {}
        elif isinstance(sizes_windows, tuple):
            sizes_windows = {Atom(): sizes_windows}
        return [
            sizes_windows.get(Atom(), (None, None))
        ] + [
            sizes_windows.get(self.mapping.id_to_marker[i], (None, None))
            for i in range(self.mapping.nb_markers())
        ]


    def set_builder(self, non_terminal, func):
        """Set the builder for a non-terminal symbol.

        Args:
            non_terminal (RuleName): the name of the non-terminal symbol.

            func (function): the builder.
        """
        symbol_id = self.mapping.rule_name_to_id[non_terminal]
        self.builders[symbol_id] = func

    def get_builder(self, non_terminal):
        """Retrieve the current builder for a non-terminal symbol.

        Args:
            non_terminal (RuleName): the name of the non-terminal symbol.

        Returns:
            function: the current builder currently bound to the rule name
                passed as argument.
        """
        symbol_id = self.mapping.rule_name_to_id[non_terminal]
        return self.builders[symbol_id]

    def sample(self, sizes_windows):
        """Generate a term of the grammar given the prescribed sizes.

        Args:
            sizes_windows (Tuple[int,int]] | Dict[(Atom|Marker),Tuple[int,int]]):
                for atoms (resp. markers) for which a size window is
                specified, the generator will only generate objects whose
                number of those atoms (resp. markers) are in the
                specified size windows. For instance a
                ``generator.sample({z: (100, 200)})`` will only generate
                objects with a number of ``z`` belonging to the
                interval `[100, 200]`.
        """
        first_rule = (
            REF,
            self.oracle_values[self.rule_name],
            self.mapping.rule_name_to_id[self.rule_name]
        )
        return c_gen(
            first_rule,
            self.flat_rules,
            self._sanitize_windows(sizes_windows),
            self.builders,
            labelling=self.grammar.labelled,
        )
