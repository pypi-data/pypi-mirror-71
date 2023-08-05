/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


#include "mm_op3.h"


// %%EXPORT p
uint32_t mm_op3_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 3.
{
    uint_fast32_t len = 7734; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}



// %%EXPORT p
uint32_t mm_op3_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 3..
//  Comparison is done modulo 3.
//  The function returns 0 in case of equality and 1 otherwise.
//  Warning: This function has not yet been tested!
{
    uint_fast32_t len = 7734;
    uint_mmv_t a, b, t, c;
    do {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0x3ULL and unsigned 2-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0x1ULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0x5555555555555555ULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0x5555555555555555ULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    } while (--len);
    return 0; 
}
   
    

// %%EXPORT p
void mm_op3_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 3.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 7734;
    uint_mmv_t a1, b1;
    uint_mmv_t a2;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a2 = ((a1 >> 2) & 0x3333333333333333ULL)
           + ((b1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL)
           + (b1 & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x1111111111111111ULL);
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x1111111111111111ULL);
        a1 = a1 + (a2 << 2);
        *mv1++ = a1;
    } while (--len);
}



// %%EXPORT p
void mm_op3_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 3.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 7734;
    uint_mmv_t a1, a2;
    factor %= 3;
    if (factor < 0) factor += 3;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL);
        a1 *= factor;
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x1111111111111111ULL);
        a2 *= factor;
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x3333333333333333ULL);
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x1111111111111111ULL);
        a1 = a1 + (a2 << 2);
        *mv1++ = a1;
    } while (--len);
}




// %%EXPORT p
uint32_t mm_op3_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 3.
//  Comparison is done modulo q. q must divide 3. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 3
{
    if (q == 3) return mm_op3_compare(mv1, mv2);
    return q == 1 ? 0 : 2;
}