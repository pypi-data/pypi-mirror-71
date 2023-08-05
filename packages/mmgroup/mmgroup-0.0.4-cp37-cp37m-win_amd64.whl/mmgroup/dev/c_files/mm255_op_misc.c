/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


#include "mm_op255.h"


// %%EXPORT p
uint32_t mm_op255_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 255.
{
    uint_fast32_t len = 30936; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}



// %%EXPORT p
uint32_t mm_op255_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 255..
//  Comparison is done modulo 255.
//  The function returns 0 in case of equality and 1 otherwise.
//  Warning: This function has not yet been tested!
{
    uint_fast32_t len = 30936;
    uint_mmv_t a, b, t, c;
    do {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0xffULL and unsigned 8-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0x7fULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0x7f7f7f7f7f7f7f7fULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0x7f7f7f7f7f7f7f7fULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    } while (--len);
    return 0; 
}
   
    

// %%EXPORT p
void mm_op255_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 255.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, b1;
    uint_mmv_t a2;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a2 = ((a1 >> 8) & 0xff00ff00ff00ffULL)
           + ((b1 >> 8) & 0xff00ff00ff00ffULL);
        a1 = (a1 & 0xff00ff00ff00ffULL)
           + (b1 & 0xff00ff00ff00ffULL);
        a1 = (a1 & 0xff00ff00ff00ffULL) 
              + ((a1 >> 8) & 0x1000100010001ULL);
        a2 = (a2 & 0xff00ff00ff00ffULL) 
              + ((a2 >> 8) & 0x1000100010001ULL);
        a1 = a1 + (a2 << 8);
        *mv1++ = a1;
    } while (--len);
}



// %%EXPORT p
void mm_op255_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 255.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, a2;
    factor %= 255;
    if (factor < 0) factor += 255;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 8) & 0xff00ff00ff00ffULL);
        a1 = (a1 & 0xff00ff00ff00ffULL);
        a1 *= factor;
        a1 = (a1 & 0xff00ff00ff00ffULL) 
              + ((a1 >> 8) & 0xff00ff00ff00ffULL);
        a1 = (a1 & 0xff00ff00ff00ffULL) 
              + ((a1 >> 8) & 0x1000100010001ULL);
        a2 *= factor;
        a2 = (a2 & 0xff00ff00ff00ffULL) 
              + ((a2 >> 8) & 0xff00ff00ff00ffULL);
        a2 = (a2 & 0xff00ff00ff00ffULL) 
              + ((a2 >> 8) & 0x1000100010001ULL);
        a1 = a1 + (a2 << 8);
        *mv1++ = a1;
    } while (--len);
}




// %%EXPORT p
uint32_t mm_op255_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 255.
//  Comparison is done modulo q. q must divide 255. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 255
{
    uint_fast32_t d1, d2, len = 30936;
    if (q == 255) return mm_op255_compare(mv1, mv2);
    if (q <= 1) return 2 - 2 * q;
    d1 = 255 / q;
    if (d1 * q != 255) return 2;
    d2 = 255 - d1;
    do {
        uint_mmv_t a, b;
        a = (*mv1 & 0xff00ff00ff00ffULL) * d1 
          + (*mv2 & 0xff00ff00ff00ffULL) * d2;
        a = (a & 0xff00ff00ff00ffULL) + ((a >> 8) & 0xff00ff00ff00ffULL);
        a = (a & 0xff00ff00ff00ffULL) + ((a >> 8) & 0xff00ff00ff00ffULL);

        b = ((*mv1++ >> 8) & 0xff00ff00ff00ffULL) * d1
          + ((*mv2++ >> 8) & 0xff00ff00ff00ffULL) * d2;
        b = (b & 0xff00ff00ff00ffULL) + ((b >> 8) & 0xff00ff00ff00ffULL);
        b = (b & 0xff00ff00ff00ffULL) + ((b >> 8) & 0xff00ff00ff00ffULL);

        a += b << 8;
        a ^= a >> 1;
        if (a & 0x7f7f7f7f7f7f7f7fULL) return 1;
    } while (--len);
    return 0;
}