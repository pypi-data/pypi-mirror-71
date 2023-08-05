
# cython: language_level=3

from __future__ import absolute_import, division, print_function
from __future__ import  unicode_literals

from cython.parallel cimport parallel
cimport openmp

from libc.stdint cimport uint32_t, uint16_t, uint8_t, int32_t
from libc.stdint cimport uint16_t
from libc.stdint cimport uint64_t as uint_mmv_t




######################################################################
### Wrappers for C functions from file mm_op31.pxd
######################################################################


cimport mm_op31

cimport cython

@cython.wraparound(False)
@cython.boundscheck(False)
def op_pi(v_in, delta, pi, v_out):
    cdef uint_mmv_t[::1] v_in_v_ = v_in
    cdef uint32_t delta_v_ = delta
    cdef uint32_t pi_v_ = pi
    cdef uint_mmv_t[::1] v_out_v_ = v_out
    with nogil:
        mm_op31.mm_op31_pi(&v_in_v_[0], delta_v_, pi_v_, &v_out_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_delta(v_in, delta, v_out):
    cdef uint_mmv_t[::1] v_in_v_ = v_in
    cdef uint32_t delta_v_ = delta
    cdef uint_mmv_t[::1] v_out_v_ = v_out
    with nogil:
        mm_op31.mm_op31_delta(&v_in_v_[0], delta_v_, &v_out_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_copy(mv1, mv2):
    cdef uint_mmv_t[::1] mv1_v_ = mv1
    cdef uint_mmv_t[::1] mv2_v_ = mv2
    cdef uint32_t ret_
    with nogil:
        ret_ = mm_op31.mm_op31_copy(&mv1_v_[0], &mv2_v_[0])
    return ret_

@cython.wraparound(False)
@cython.boundscheck(False)
def op_compare(mv1, mv2):
    cdef uint_mmv_t[::1] mv1_v_ = mv1
    cdef uint_mmv_t[::1] mv2_v_ = mv2
    cdef uint32_t ret_
    with nogil:
        ret_ = mm_op31.mm_op31_compare(&mv1_v_[0], &mv2_v_[0])
    return ret_

@cython.wraparound(False)
@cython.boundscheck(False)
def op_vector_add(mv1, mv2):
    cdef uint_mmv_t[::1] mv1_v_ = mv1
    cdef uint_mmv_t[::1] mv2_v_ = mv2
    with nogil:
        mm_op31.mm_op31_vector_add(&mv1_v_[0], &mv2_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_scalar_mul(factor, mv1):
    cdef int32_t factor_v_ = factor
    cdef uint_mmv_t[::1] mv1_v_ = mv1
    with nogil:
        mm_op31.mm_op31_scalar_mul(factor_v_, &mv1_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_compare_mod_q(mv1, mv2, q):
    cdef uint_mmv_t[::1] mv1_v_ = mv1
    cdef uint_mmv_t[::1] mv2_v_ = mv2
    cdef uint32_t q_v_ = q
    cdef uint32_t ret_
    with nogil:
        ret_ = mm_op31.mm_op31_compare_mod_q(&mv1_v_[0], &mv2_v_[0], q_v_)
    return ret_

@cython.wraparound(False)
@cython.boundscheck(False)
def op_xy(v_in, f, e, eps, v_out):
    cdef uint_mmv_t[::1] v_in_v_ = v_in
    cdef uint32_t f_v_ = f
    cdef uint32_t e_v_ = e
    cdef uint32_t eps_v_ = eps
    cdef uint_mmv_t[::1] v_out_v_ = v_out
    with nogil:
        mm_op31.mm_op31_xy(&v_in_v_[0], f_v_, e_v_, eps_v_, &v_out_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_t(v_in, exp, v_out):
    cdef uint_mmv_t[::1] v_in_v_ = v_in
    cdef uint32_t exp_v_ = exp
    cdef uint_mmv_t[::1] v_out_v_ = v_out
    with nogil:
        mm_op31.mm_op31_t(&v_in_v_[0], exp_v_, &v_out_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_xi(v_in, exp, v_out):
    cdef uint_mmv_t[::1] v_in_v_ = v_in
    cdef uint32_t exp_v_ = exp
    cdef uint_mmv_t[::1] v_out_v_ = v_out
    with nogil:
        mm_op31.mm_op31_xi(&v_in_v_[0], exp_v_, &v_out_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_group_n(v, g, work):
    cdef uint_mmv_t[::1] v_v_ = v
    cdef uint32_t[::1] g_v_ = g
    cdef uint_mmv_t[::1] work_v_ = work
    with nogil:
        mm_op31.mm_op31_group_n(&v_v_[0], &g_v_[0], &work_v_[0])

@cython.wraparound(False)
@cython.boundscheck(False)
def op_word(v, g, len_g, e, work):
    cdef uint_mmv_t[::1] v_v_ = v
    cdef uint32_t[::1] g_v_ = g
    cdef int32_t len_g_v_ = len_g
    cdef int32_t e_v_ = e
    cdef uint_mmv_t[::1] work_v_ = work
    with nogil:
        mm_op31.mm_op31_word(&v_v_[0], &g_v_[0], len_g_v_, e_v_, &work_v_[0])


######################################################################
### Constants
######################################################################


MMV_ENTRIES = 247488

INT_BITS = 64

LOG_INT_BITS = 6

P = 31

FIELD_BITS = 8

LOG_FIELD_BITS = 3

INT_FIELDS = 8

LOG_INT_FIELDS = 3

P_BITS = 5

MMV_INTS = 30936

