/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


#include "mm_op31.h"


// %%EXPORT p
uint32_t mm_op31_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 31.
{
    uint_fast32_t len = 30936; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}



// %%EXPORT p
uint32_t mm_op31_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 31..
//  Comparison is done modulo 31.
//  The function returns 0 in case of equality and 1 otherwise.
//  Warning: This function has not yet been tested!
{
    uint_fast32_t len = 30936;
    uint_mmv_t a, b, t, c;
    do {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0x1fULL and unsigned 5-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0xfULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0xf0f0f0f0f0f0f0fULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0xf0f0f0f0f0f0f0fULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    } while (--len);
    return 0; 
}
   
    

// %%EXPORT p
void mm_op31_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 31.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, b1;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a1 = (a1 & 0x1f1f1f1f1f1f1f1fULL) 
              + (b1 & 0x1f1f1f1f1f1f1f1fULL);                     
        a1 = (a1 & 0x1f1f1f1f1f1f1f1fULL) 
              + ((a1 >> 5) & 0x101010101010101ULL);
        *mv1++ = a1;
    } while (--len);
}



// %%EXPORT p
void mm_op31_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 31.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, a2;
    factor %= 31;
    if (factor < 0) factor += 31;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 8) & 0x1f001f001f001fULL);
        a1 = (a1 & 0x1f001f001f001fULL);
        a1 *= factor;
        a1 = (a1 & 0x1f001f001f001fULL) 
              + ((a1 >> 5) & 0x1f001f001f001fULL);
        a1 = (a1 & 0x1f001f001f001fULL) 
              + ((a1 >> 5) & 0x1000100010001ULL);
        a2 *= factor;
        a2 = (a2 & 0x1f001f001f001fULL) 
              + ((a2 >> 5) & 0x1f001f001f001fULL);
        a2 = (a2 & 0x1f001f001f001fULL) 
              + ((a2 >> 5) & 0x1000100010001ULL);
        a1 = a1 + (a2 << 8);
        *mv1++ = a1;
    } while (--len);
}




// %%EXPORT p
uint32_t mm_op31_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 31.
//  Comparison is done modulo q. q must divide 31. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 31
{
    if (q == 31) return mm_op31_compare(mv1, mv2);
    return q == 1 ? 0 : 2;
}