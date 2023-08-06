# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from libc.stdint cimport uint64_t, int64_t

cdef extern from "xoshiro.h":
    ctypedef uint64_t randstate[4];

    double rand_double()
    int64_t rand_i64(const int64_t bound)

    void seed(const uint64_t seed)
    void get_state(uint64_t dest[4])
    void set_state(const uint64_t s[4])
