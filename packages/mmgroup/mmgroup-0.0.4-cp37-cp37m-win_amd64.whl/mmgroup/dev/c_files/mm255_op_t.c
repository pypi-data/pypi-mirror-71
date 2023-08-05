/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

// %%COMMENT
// TODO: Yet to be documented!!!


#include <string.h>
#include "mat24_functions.h"
#include "mm_op255.h"   



static void invert255_xyz(uint_mmv_t *v_in, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    const uint16_t *p_theta = MAT24_THETA_TABLE;
    
    for (i = 0; i <2048; ++i) {
        uint_mmv_t mask = -((uint_mmv_t)(((p_theta[i] >> 12) & 0x1ULL)));
        mask &= 0xffffffffffffffffULL;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = *v_in++ ^ mask;
        *v_out++ = 0;
        ++v_in;
    }
}


// %%EXPORT p
void mm_op255_t(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, j, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 30936; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 = 0x1ULL - (uint_mmv_t)exp;

    // Do off-diagonal part of tags A, B, C
    for (i = 0; i < 24; ++i) {
        for (j = 0; j < 3; ++j) {
            // %%MUL_MATRIX_T3 v_in, exp1, v_out

            // This is an automatically generated matrix operation, do not change!
            {
            uint_mmv_t r0, r1, r2, r3, r4;
            uint_mmv_t r5, r6;

            // Multiply the vector of integers mod 255 stored in
            // (v_in) by t**e, where t is the 3 times 3 triality
            // matrix [[0, 2,  -2], [1, 1, 1], [1,  -1, -1]] / 2.
            // and e = 1 if exp1 = 0, e = 2 if exp1 = 
            // (uint_mmv_t)(-1). The result is stored in (v_out).
            // 
            // v_in and v_out are pointers of type *uint_mmv_t.
            // Components with tags A, B, C referred by (v_in) 
            // are processed, one integer of type uint_mmv_t
            // for each tag.
            // 
            // 
            // Loading vector from rep 196884x with tags A,B,C
            // to v[0...2]. Here v_in refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            r0 = (v_in)[0];
            r1 = (v_in)[96];
            r2 = (v_in)[192] ^ ((exp1) & 0xffffffffffffffffULL);
            // Vector is now  r(i) for i = 0,1,2,3,4,5
            exp1 = ~(exp1);
            r3 = ((r0 >> 8) & 0xff00ff00ff00ffULL);
            r0 = (r0 & 0xff00ff00ff00ffULL);
            r4 = ((r1 >> 8) & 0xff00ff00ff00ffULL);
            r1 = (r1 & 0xff00ff00ff00ffULL);
            r5 = ((r2 >> 8) & 0xff00ff00ff00ffULL);
            r2 = (r2 & 0xff00ff00ff00ffULL);
            r6 = (r4 + (r5 ^ 0xff00ff00ff00ffULL));
            r4 = (r4 + r5);
            r5 = (r6 & 0x100010001000100ULL);
            r5 = ((r6 - r5) + (r5 >> 8));
            r6 = (r4 & 0x100010001000100ULL);
            r4 = ((r4 - r6) + (r6 >> 8));
            r4 = (((r4 & 0x101010101010101ULL) << 7)
                | ((r4 & 0xfefefefefefefefeULL) >> 1));
            r5 = (((r5 & 0x101010101010101ULL) << 7)
                | ((r5 & 0xfefefefefefefefeULL) >> 1));
            r6 = (r3 + (r5 ^ 0xff00ff00ff00ffULL));
            r3 = (r3 + r5);
            r5 = (r6 & 0x100010001000100ULL);
            r5 = ((r6 - r5) + (r5 >> 8));
            r6 = (r3 & 0x100010001000100ULL);
            r3 = ((r3 - r6) + (r6 >> 8));
            r6 = (r1 + (r2 ^ 0xff00ff00ff00ffULL));
            r1 = (r1 + r2);
            r2 = (r6 & 0x100010001000100ULL);
            r2 = ((r6 - r2) + (r2 >> 8));
            r6 = (r1 & 0x100010001000100ULL);
            r1 = ((r1 - r6) + (r6 >> 8));
            r1 = (((r1 & 0x101010101010101ULL) << 7)
                | ((r1 & 0xfefefefefefefefeULL) >> 1));
            r2 = (((r2 & 0x101010101010101ULL) << 7)
                | ((r2 & 0xfefefefefefefefeULL) >> 1));
            r6 = (r0 + (r2 ^ 0xff00ff00ff00ffULL));
            r0 = (r0 + r2);
            r2 = (r6 & 0x100010001000100ULL);
            r2 = ((r6 - r2) + (r2 >> 8));
            r6 = (r0 & 0x100010001000100ULL);
            r0 = ((r0 - r6) + (r6 >> 8));
            r0 ^= (r3 << 8);
            r1 ^= (r4 << 8);
            r2 ^= (r5 << 8);
            // Store vector v[0...2] to rep 196884x with 
            // tags A,B,C. Here v_out refers to the tag A part. 
            // Negate v[2] if exp1 == -1.
            (v_out)[0] = r1;
            (v_out)[96] = r0;
            (v_out)[192]  = r2 ^ ((exp1) & 0xffffffffffffffffULL);
            exp1 = ~(exp1);
            // 45 lines of code, 85 operations
            }
            // End of automatically generated matrix operation.
 
            ++v_in; ++v_out;
        }
        ++v_in;
        *v_out++ = 0;
    }

    v_in -= 96;
    v_out -= 96;
    // Do diagonal part of tags A, B, C
    for (i = 0; i < 24; ++i) {
        // Copy diagonal of A, zero diagonals of B and C
        uint_mmv_t mask = 0xffULL << ((i << 3) & 63);
        j = (i << 2) + (i >> 3);
        v_out[j] = (v_out[j] & ~mask) | (v_in[j] & mask);
        v_out[j + 96] &= ~mask;
        v_out[j + 192] &= ~mask;
    }


    // Do tag T
    v_in += MM_OP255_OFS_T;
    v_out +=  MM_OP255_OFS_T;
    for (i = 0; i < 759; ++i) {
        // %%MUL_MATRIX_T64 v_in, exp1, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;
        uint_mmv_t r10, r11, r12, r13, r14;
        uint_mmv_t r15, r16;

        // Multiply the vector of integers mod 255 stored
        // in (v_in) by t**e, where t is the 64 times 64 
        // triality matrix and e = 1 if exp1 = 0, e = 2 if
        // exp1 = (uint_mmv_t)(-1). The result is stored
        // in (v_out).
        // 
        // Loading vector v from array v_in; multiply v
        // with diagonal matrix if exp1 == -1.
        r0 = v_in[0] ^ ((exp1) & 0xffffffffffff00ULL);
        r1 = v_in[1] ^ ((exp1) & 0xff00ffffffULL);
        r2 = v_in[2] ^ ((exp1) & 0xff00ffffffULL);
        r3 = v_in[3] ^ ((exp1) & 0xff000000000000ffULL);
        r4 = v_in[4] ^ ((exp1) & 0xff00ffffffULL);
        r5 = v_in[5] ^ ((exp1) & 0xff000000000000ffULL);
        r6 = v_in[6] ^ ((exp1) & 0xff000000000000ffULL);
        r7 = v_in[7] ^ ((exp1) & 0xffffff00ff000000ULL);
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        exp1 = ~(exp1);
        // Exchange component i with component 63-i if i 
        // has odd parity; fix it if i has even parity.
        r8 = ((r0 & 0xff0000ff00ffff00ULL)
            | (r7 & 0xffff00ff0000ffULL));
        r8 = ((r8 << 32) | (r8 >> 32));
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL));
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL));
        r0 = ((r0 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL));
        r7 = ((r7 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL));
        r8 = ((r1 & 0xffff00ff0000ffULL)
            | (r6 & 0xff0000ff00ffff00ULL));
        r8 = ((r8 << 32) | (r8 >> 32));
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL));
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL));
        r1 = ((r1 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL));
        r6 = ((r6 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL));
        r8 = ((r2 & 0xffff00ff0000ffULL)
            | (r5 & 0xff0000ff00ffff00ULL));
        r8 = ((r8 << 32) | (r8 >> 32));
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL));
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL));
        r2 = ((r2 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL));
        r5 = ((r5 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL));
        r8 = ((r3 & 0xff0000ff00ffff00ULL)
            | (r4 & 0xffff00ff0000ffULL));
        r8 = ((r8 << 32) | (r8 >> 32));
        r8 = (((r8 & 0xffff0000ffffULL) << 16)
            | ((r8 >> 16) & 0xffff0000ffffULL));
        r8 = (((r8 & 0xff00ff00ff00ffULL) << 8)
            | ((r8 >> 8) & 0xff00ff00ff00ffULL));
        r3 = ((r3 & 0xffff00ff0000ffULL)
            | (r8 & 0xff0000ff00ffff00ULL));
        r4 = ((r4 & 0xff0000ff00ffff00ULL)
            | (r8 & 0xffff00ff0000ffULL));
        // Expansion for Hadamard operation:
        // There is no space for a carry bit between bit fields. So 
        // we move bit field 2*i + 1  to bit field 2*i + 64.
        r8 = ((r0 >> 8) & 0xff00ff00ff00ffULL);
        r0 = (r0 & 0xff00ff00ff00ffULL);
        r9 = ((r1 >> 8) & 0xff00ff00ff00ffULL);
        r1 = (r1 & 0xff00ff00ff00ffULL);
        r10 = ((r2 >> 8) & 0xff00ff00ff00ffULL);
        r2 = (r2 & 0xff00ff00ff00ffULL);
        r11 = ((r3 >> 8) & 0xff00ff00ff00ffULL);
        r3 = (r3 & 0xff00ff00ff00ffULL);
        r12 = ((r4 >> 8) & 0xff00ff00ff00ffULL);
        r4 = (r4 & 0xff00ff00ff00ffULL);
        r13 = ((r5 >> 8) & 0xff00ff00ff00ffULL);
        r5 = (r5 & 0xff00ff00ff00ffULL);
        r14 = ((r6 >> 8) & 0xff00ff00ff00ffULL);
        r6 = (r6 & 0xff00ff00ff00ffULL);
        r15 = ((r7 >> 8) & 0xff00ff00ff00ffULL);
        r7 = (r7 & 0xff00ff00ff00ffULL);
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r16 = (((r0 << 16) & 0xff000000ff0000ULL)
            | ((r0 & 0xff000000ff0000ULL) >> 16));
        r0 = ((r0 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = (((r1 << 16) & 0xff000000ff0000ULL)
            | ((r1 & 0xff000000ff0000ULL) >> 16));
        r1 = ((r1 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8));
        r16 = (((r2 << 16) & 0xff000000ff0000ULL)
            | ((r2 & 0xff000000ff0000ULL) >> 16));
        r2 = ((r2 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8));
        r16 = (((r3 << 16) & 0xff000000ff0000ULL)
            | ((r3 & 0xff000000ff0000ULL) >> 16));
        r3 = ((r3 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8));
        r16 = (((r4 << 16) & 0xff000000ff0000ULL)
            | ((r4 & 0xff000000ff0000ULL) >> 16));
        r4 = ((r4 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8));
        r16 = (((r5 << 16) & 0xff000000ff0000ULL)
            | ((r5 & 0xff000000ff0000ULL) >> 16));
        r5 = ((r5 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8));
        r16 = (((r6 << 16) & 0xff000000ff0000ULL)
            | ((r6 & 0xff000000ff0000ULL) >> 16));
        r6 = ((r6 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8));
        r16 = (((r7 << 16) & 0xff000000ff0000ULL)
            | ((r7 & 0xff000000ff0000ULL) >> 16));
        r7 = ((r7 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8));
        r16 = (((r8 << 16) & 0xff000000ff0000ULL)
            | ((r8 & 0xff000000ff0000ULL) >> 16));
        r8 = ((r8 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8));
        r16 = (((r9 << 16) & 0xff000000ff0000ULL)
            | ((r9 & 0xff000000ff0000ULL) >> 16));
        r9 = ((r9 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8));
        r16 = (((r10 << 16) & 0xff000000ff0000ULL)
            | ((r10 & 0xff000000ff0000ULL) >> 16));
        r10 = ((r10 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8));
        r16 = (((r11 << 16) & 0xff000000ff0000ULL)
            | ((r11 & 0xff000000ff0000ULL) >> 16));
        r11 = ((r11 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8));
        r16 = (((r12 << 16) & 0xff000000ff0000ULL)
            | ((r12 & 0xff000000ff0000ULL) >> 16));
        r12 = ((r12 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8));
        r16 = (((r13 << 16) & 0xff000000ff0000ULL)
            | ((r13 & 0xff000000ff0000ULL) >> 16));
        r13 = ((r13 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8));
        r16 = (((r14 << 16) & 0xff000000ff0000ULL)
            | ((r14 & 0xff000000ff0000ULL) >> 16));
        r14 = ((r14 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8));
        r16 = (((r15 << 16) & 0xff000000ff0000ULL)
            | ((r15 & 0xff000000ff0000ULL) >> 16));
        r15 = ((r15 ^ 0xff000000ff0000ULL) + r16);
        r16 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+4] = v[i]+v[i+4], v[i]-v[i+4]
        r16 = ((r0 << 32) | (r0 >> 32));
        r0 = ((r0 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = ((r1 << 32) | (r1 >> 32));
        r1 = ((r1 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8));
        r16 = ((r2 << 32) | (r2 >> 32));
        r2 = ((r2 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8));
        r16 = ((r3 << 32) | (r3 >> 32));
        r3 = ((r3 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8));
        r16 = ((r4 << 32) | (r4 >> 32));
        r4 = ((r4 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8));
        r16 = ((r5 << 32) | (r5 >> 32));
        r5 = ((r5 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8));
        r16 = ((r6 << 32) | (r6 >> 32));
        r6 = ((r6 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8));
        r16 = ((r7 << 32) | (r7 >> 32));
        r7 = ((r7 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8));
        r16 = ((r8 << 32) | (r8 >> 32));
        r8 = ((r8 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8));
        r16 = ((r9 << 32) | (r9 >> 32));
        r9 = ((r9 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8));
        r16 = ((r10 << 32) | (r10 >> 32));
        r10 = ((r10 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8));
        r16 = ((r11 << 32) | (r11 >> 32));
        r11 = ((r11 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8));
        r16 = ((r12 << 32) | (r12 >> 32));
        r12 = ((r12 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8));
        r16 = ((r13 << 32) | (r13 >> 32));
        r13 = ((r13 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8));
        r16 = ((r14 << 32) | (r14 >> 32));
        r14 = ((r14 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8));
        r16 = ((r15 << 32) | (r15 >> 32));
        r15 = ((r15 ^ 0xff00ff00000000ULL) + r16);
        r16 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r16 = (r0 + (r1 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r1);
        r1 = (r16 & 0x100010001000100ULL);
        r1 = ((r16 - r1) + (r1 >> 8));
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = (r2 + (r3 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r3);
        r3 = (r16 & 0x100010001000100ULL);
        r3 = ((r16 - r3) + (r3 >> 8));
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8));
        r16 = (r4 + (r5 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r5);
        r5 = (r16 & 0x100010001000100ULL);
        r5 = ((r16 - r5) + (r5 >> 8));
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8));
        r16 = (r6 + (r7 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8));
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8));
        r16 = (r8 + (r9 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r9);
        r9 = (r16 & 0x100010001000100ULL);
        r9 = ((r16 - r9) + (r9 >> 8));
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8));
        r16 = (r10 + (r11 ^ 0xff00ff00ff00ffULL));
        r10 = (r10 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8));
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8));
        r16 = (r12 + (r13 ^ 0xff00ff00ff00ffULL));
        r12 = (r12 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8));
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8));
        r16 = (r14 + (r15 ^ 0xff00ff00ff00ffULL));
        r14 = (r14 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8));
        r16 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r16 = (r0 + (r2 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r2);
        r2 = (r16 & 0x100010001000100ULL);
        r2 = ((r16 - r2) + (r2 >> 8));
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = (r1 + (r3 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r3);
        r3 = (r16 & 0x100010001000100ULL);
        r3 = ((r16 - r3) + (r3 >> 8));
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8));
        r16 = (r4 + (r6 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r6);
        r6 = (r16 & 0x100010001000100ULL);
        r6 = ((r16 - r6) + (r6 >> 8));
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8));
        r16 = (r5 + (r7 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8));
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8));
        r16 = (r8 + (r10 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r10);
        r10 = (r16 & 0x100010001000100ULL);
        r10 = ((r16 - r10) + (r10 >> 8));
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8));
        r16 = (r9 + (r11 ^ 0xff00ff00ff00ffULL));
        r9 = (r9 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8));
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8));
        r16 = (r12 + (r14 ^ 0xff00ff00ff00ffULL));
        r12 = (r12 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8));
        r16 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r16) + (r16 >> 8));
        r16 = (r13 + (r15 ^ 0xff00ff00ff00ffULL));
        r13 = (r13 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8));
        r16 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r16 = (r0 + (r4 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r4);
        r4 = (r16 & 0x100010001000100ULL);
        r4 = ((r16 - r4) + (r4 >> 8));
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = (r1 + (r5 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r5);
        r5 = (r16 & 0x100010001000100ULL);
        r5 = ((r16 - r5) + (r5 >> 8));
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8));
        r16 = (r2 + (r6 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r6);
        r6 = (r16 & 0x100010001000100ULL);
        r6 = ((r16 - r6) + (r6 >> 8));
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8));
        r16 = (r3 + (r7 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r7);
        r7 = (r16 & 0x100010001000100ULL);
        r7 = ((r16 - r7) + (r7 >> 8));
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8));
        r16 = (r8 + (r12 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r12);
        r12 = (r16 & 0x100010001000100ULL);
        r12 = ((r16 - r12) + (r12 >> 8));
        r16 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r16) + (r16 >> 8));
        r16 = (r9 + (r13 ^ 0xff00ff00ff00ffULL));
        r9 = (r9 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8));
        r16 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r16) + (r16 >> 8));
        r16 = (r10 + (r14 ^ 0xff00ff00ff00ffULL));
        r10 = (r10 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8));
        r16 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r16) + (r16 >> 8));
        r16 = (r11 + (r15 ^ 0xff00ff00ff00ffULL));
        r11 = (r11 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8));
        r16 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r16 = (r0 + (r8 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r8);
        r8 = (r16 & 0x100010001000100ULL);
        r8 = ((r16 - r8) + (r8 >> 8));
        r16 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r16) + (r16 >> 8));
        r16 = (r1 + (r9 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r9);
        r9 = (r16 & 0x100010001000100ULL);
        r9 = ((r16 - r9) + (r9 >> 8));
        r16 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r16) + (r16 >> 8));
        r16 = (r2 + (r10 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r10);
        r10 = (r16 & 0x100010001000100ULL);
        r10 = ((r16 - r10) + (r10 >> 8));
        r16 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r16) + (r16 >> 8));
        r16 = (r3 + (r11 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r11);
        r11 = (r16 & 0x100010001000100ULL);
        r11 = ((r16 - r11) + (r11 >> 8));
        r16 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r16) + (r16 >> 8));
        r16 = (r4 + (r12 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r12);
        r12 = (r16 & 0x100010001000100ULL);
        r12 = ((r16 - r12) + (r12 >> 8));
        r16 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r16) + (r16 >> 8));
        r16 = (r5 + (r13 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r13);
        r13 = (r16 & 0x100010001000100ULL);
        r13 = ((r16 - r13) + (r13 >> 8));
        r16 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r16) + (r16 >> 8));
        r16 = (r6 + (r14 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r14);
        r14 = (r16 & 0x100010001000100ULL);
        r14 = ((r16 - r14) + (r14 >> 8));
        r16 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r16) + (r16 >> 8));
        r16 = (r7 + (r15 ^ 0xff00ff00ff00ffULL));
        r7 = (r7 + r15);
        r15 = (r16 & 0x100010001000100ULL);
        r15 = ((r16 - r15) + (r15 >> 8));
        r16 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r16) + (r16 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Reverse expansion for Hadamard operation
        r0 ^= (r8 << 8);
        r1 ^= (r9 << 8);
        r2 ^= (r10 << 8);
        r3 ^= (r11 << 8);
        r4 ^= (r12 << 8);
        r5 ^= (r13 << 8);
        r6 ^= (r14 << 8);
        r7 ^= (r15 << 8);
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Multiply vector by scalar 2**-3 mod 255
        r0 = (((r0 & 0x707070707070707ULL) << 5)
            | ((r0 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r1 = (((r1 & 0x707070707070707ULL) << 5)
            | ((r1 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r2 = (((r2 & 0x707070707070707ULL) << 5)
            | ((r2 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r3 = (((r3 & 0x707070707070707ULL) << 5)
            | ((r3 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r4 = (((r4 & 0x707070707070707ULL) << 5)
            | ((r4 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r5 = (((r5 & 0x707070707070707ULL) << 5)
            | ((r5 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r6 = (((r6 & 0x707070707070707ULL) << 5)
            | ((r6 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        r7 = (((r7 & 0x707070707070707ULL) << 5)
            | ((r7 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        // Storing vector v to array v_out; multiply v
        // with diagonal matrix if exp1 == -1.
        v_out[0] = r0 ^ ((exp1) & 0xffffffffffff00ULL);
        v_out[1] = r1 ^ ((exp1) & 0xff00ffffffULL);
        v_out[2] = r2 ^ ((exp1) & 0xff00ffffffULL);
        v_out[3] = r3 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[4] = r4 ^ ((exp1) & 0xff00ffffffULL);
        v_out[5] = r5 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[6] = r6 ^ ((exp1) & 0xff000000000000ffULL);
        v_out[7] = r7 ^ ((exp1) & 0xffffff00ff000000ULL);
        exp1 = ~(exp1);
        // 394 lines of code, 874 operations
        }
        // End of automatically generated matrix operation.
 
        v_in += 8;
        v_out += 8;
    }

    // Do tags X, Y, and Z
    {
         uint_mmv_t *pXYin, *pYZin, *pZXin;
         uint_mmv_t *pXYout, *pYZout, *pZXout;
         if (exp1 == 0) {
             pXYin = v_in; 
             pXYout = v_out + 16384;  
             pYZin = v_in + 16384; 
             pYZout = v_out + 8192;  
             pZXin = v_in + 8192; 
             pZXout = v_out; 
         } else {
             pXYout = v_out; 
             pXYin = v_in + 16384;  
             pYZout = v_out + 16384; 
             pYZin = v_in + 8192;  
             pZXout = v_out + 8192; 
             pZXin = v_in; 
         }

         // Map X to Y for t and Y to X for t**2
         for (i = 0; i < 8192; ++i) pXYout[i] = pXYin[i];
         mm255_neg_scalprod_d_i(pXYout);
         
         // Map Y to Z for t and Z to Y for t**2
         invert255_xyz(pYZin, pYZout);
         mm255_neg_scalprod_d_i(pYZout);

         // Map Z to X for t and X to Z for t**2
         invert255_xyz(pZXin, pZXout);
    }
}


