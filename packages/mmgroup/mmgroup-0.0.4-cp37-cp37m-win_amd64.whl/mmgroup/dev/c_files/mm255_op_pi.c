/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


// %%COMMENT
// TODO: Adjust this to new order of basis vectors rep!!!

#include <string.h>
#include "mm_op255.h"   




   
static const uint_mmv_t MM255_TBL_SCALPROD_HIGH[] = { 
// %%TABLE MMV_TBL_SCALPROD_HIGH, uint{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffff000000000000ULL,0xffff000000000000ULL,
0x00ffff00ff00ff00ULL,0x0000000000000000ULL,
0xff00ff0000000000ULL,0xff00ff0000000000ULL,
0xffff000000ffff00ULL,0x0000000000000000ULL,
0x00ffff0000000000ULL,0x00ffff0000000000ULL,
0xff00ff00ffff0000ULL,0x0000000000000000ULL,
0x00000000ffff0000ULL,0xffff000000000000ULL,
0xff00ff0000ffff00ULL,0x0000000000000000ULL,
0xffff0000ffff0000ULL,0x0000000000000000ULL,
0xffff0000ffff0000ULL,0x0000000000000000ULL,
0xff00ff00ffff0000ULL,0x00ffff0000000000ULL,
0x00ffff0000000000ULL,0x0000000000000000ULL,
0x00ffff00ffff0000ULL,0xff00ff0000000000ULL,
0x00000000ff00ff00ULL,0x0000000000000000ULL,
0x00000000ff00ff00ULL,0xff00ff0000000000ULL,
0x00ffff00ffff0000ULL,0x0000000000000000ULL,
0xffff0000ff00ff00ULL,0x00ffff0000000000ULL,
0x0000000000ffff00ULL,0x0000000000000000ULL,
0xff00ff00ff00ff00ULL,0x0000000000000000ULL,
0xff00ff00ff00ff00ULL,0x0000000000000000ULL,
0x00ffff00ff00ff00ULL,0xffff000000000000ULL,
0xffff000000000000ULL,0x0000000000000000ULL,
0x0000000000ffff00ULL,0x00ffff0000000000ULL,
0xffff0000ff00ff00ULL,0x0000000000000000ULL,
0xffff000000ffff00ULL,0xff00ff0000000000ULL,
0xff00ff0000000000ULL,0x0000000000000000ULL,
0xff00ff0000ffff00ULL,0xffff000000000000ULL,
0x00000000ffff0000ULL,0x0000000000000000ULL,
0x00ffff0000ffff00ULL,0x0000000000000000ULL,
0x00ffff0000ffff00ULL,0x0000000000000000ULL,
0x000000ffffffff00ULL,0x000000ff000000ffULL,
0x000000ff000000ffULL,0x0000000000000000ULL,
0xffff00ffffffff00ULL,0xffff00ff000000ffULL,
0x00ffffffff00ffffULL,0x0000000000000000ULL,
0xff00ffffffffff00ULL,0xff00ffff000000ffULL,
0xffff00ff00ffffffULL,0x0000000000000000ULL,
0x00ffffffffffff00ULL,0x00ffffff000000ffULL,
0xff00ffffffff00ffULL,0x0000000000000000ULL,
0x000000ff0000ff00ULL,0xffff00ff000000ffULL,
0xff00ffff00ffffffULL,0x0000000000000000ULL,
0xffff00ff0000ff00ULL,0x000000ff000000ffULL,
0xffff00ffffff00ffULL,0x0000000000000000ULL,
0xff00ffff0000ff00ULL,0x00ffffff000000ffULL,
0x00ffffff000000ffULL,0x0000000000000000ULL,
0x00ffffff0000ff00ULL,0xff00ffff000000ffULL,
0x000000ffff00ffffULL,0x0000000000000000ULL,
0x000000ff00ff0000ULL,0xff00ffff000000ffULL,
0x00ffffffffff00ffULL,0x0000000000000000ULL,
0xffff00ff00ff0000ULL,0x00ffffff000000ffULL,
0x000000ff00ffffffULL,0x0000000000000000ULL,
0xff00ffff00ff0000ULL,0x000000ff000000ffULL,
0xff00ffffff00ffffULL,0x0000000000000000ULL,
0x00ffffff00ff0000ULL,0xffff00ff000000ffULL,
0xffff00ff000000ffULL,0x0000000000000000ULL,
0x000000ffff000000ULL,0x00ffffff000000ffULL,
0xffff00ffff00ffffULL,0x0000000000000000ULL,
0xffff00ffff000000ULL,0xff00ffff000000ffULL,
0xff00ffff000000ffULL,0x0000000000000000ULL,
0xff00ffffff000000ULL,0xffff00ff000000ffULL,
0x000000ffffff00ffULL,0x0000000000000000ULL,
0x00ffffffff000000ULL,0x000000ff000000ffULL,
0x00ffffff00ffffffULL,0x0000000000000000ULL
};

static const uint_mmv_t MM255_TBL_SCALPROD_LOW[] = { 
// %%TABLE MMV_TBL_SCALPROD_LOW, uint{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0xffffffffffffffffULL,
0xffffffff00000000ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0xffffffffffffffffULL,
0x00000000ffffffffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffffffffffffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0xffff0000ffff0000ULL,
0xffff0000ffff0000ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0x0000ffff0000ffffULL,
0x0000ffffffff0000ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0x0000ffff0000ffffULL,
0xffff00000000ffffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0xffff0000ffff0000ULL,
0x0000ffff0000ffffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0xff00ff00ff00ff00ULL,
0xff00ff00ff00ff00ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0x00ff00ff00ff00ffULL,
0x00ff00ffff00ff00ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0x00ff00ff00ff00ffULL,
0xff00ff0000ff00ffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0xff00ff00ff00ff00ULL,
0x00ff00ff00ff00ffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0xff0000ffff0000ffULL,
0xff0000ff00ffff00ULL,0x0000000000000000ULL,
0xffffffff00000000ULL,0xff0000ffff0000ffULL,
0x00ffff00ff0000ffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x00ffff0000ffff00ULL,
0xff0000ffff0000ffULL,0x0000000000000000ULL
};




// %%EXPORT
void mm255_neg_scalprod_d_i(uint_mmv_t* v)
// negate entries d (x) i with sclar product equal to 1
{
    const uint_mmv_t* p0 = MM255_TBL_SCALPROD_HIGH;
    const uint_mmv_t* p0_end = p0 + 32 * 4;

    // inversion of entries (d (x) i) with scalar product 1
    for (; p0 < p0_end; p0 += 4) {
        const uint_mmv_t* p1 = MM255_TBL_SCALPROD_LOW;
        const uint_mmv_t* p1_end = p1 + 16 * 4;
        for (; p1 < p1_end; p1 += 4) {
            // %%SCALAR_PROD_2048_UNROLL p0, p1, v 
            uint_mmv_t v_t;
            v[0] ^= (v_t = p0[0] ^ p1[0]);
            v[4] ^= v_t ^ 0xffffffff00000000ULL;
            v[8] ^= v_t ^ 0xffffffff00000000ULL;
            v[12] ^= v_t ^ 0x0ULL;
            v[1] ^= (v_t = p0[1] ^ p1[1]);
            v[5] ^= v_t ^ 0xffffffff00000000ULL;
            v[9] ^= v_t ^ 0xffffffffULL;
            v[13] ^= v_t ^ 0xffffffffffffffffULL;
            v[2] ^= (v_t = p0[2] ^ p1[2]);
            v[6] ^= v_t ^ 0xffffffffffffffffULL;
            v[10] ^= v_t ^ 0xffffffffffffffffULL;
            v[14] ^= v_t ^ 0x0ULL;
            v +=   4 * 4;
        }
    }
}



// %%IF PERM24_USE_BENES_NET

static void pi24_2048(
   uint_mmv_t * p_src,
   uint16_t * p_perm,
   uint_mmv_t * benes_mask,
   uint_fast32_t sign_shift,
   uint_mmv_t * p_dest
)
{
    uint_fast32_t i1;
    for (i1 = 0; i1 < 2048; i1 += 4) {
        uint_mmv_t sgn_perm0 = p_perm[0];
        uint_mmv_t *ps0 = p_src + ((sgn_perm0 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v00, v01, v02;
        uint_mmv_t sgn_perm1 = p_perm[1];
        uint_mmv_t *ps1 = p_src + ((sgn_perm1 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v10, v11, v12;
        uint_mmv_t sgn_perm2 = p_perm[2];
        uint_mmv_t *ps2 = p_src + ((sgn_perm2 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v20, v21, v22;
        uint_mmv_t sgn_perm3 = p_perm[3];
        uint_mmv_t *ps3 = p_src + ((sgn_perm3 & 0x7ff) << 2);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v30, v31, v32;

        // Load 'ps' to temporary variables v00,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v00 = (ps0)[0];
        v01 = (ps0)[1];
        v02 = (ps0)[2];
        // Load 'ps' to temporary variables v10,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v10 = (ps1)[0];
        v11 = (ps1)[1];
        v12 = (ps1)[2];
        // Load 'ps' to temporary variables v20,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v20 = (ps2)[0];
        v21 = (ps2)[1];
        v22 = (ps2)[2];
        // Load 'ps' to temporary variables v30,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v30 = (ps3)[0];
        v31 = (ps3)[1];
        v32 = (ps3)[2];

        sgn_perm0 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
        // Permute the 24 small integers in '(v00, v01, v02)' 
        // using the Benes network given by 'benes_mask'. All small   
        // integers are negated if bit 0 of 'sign' is set.
        sgn_perm0 = (-(sgn_perm0 & 0x1ULL)) & 0xffffffffffffffffULL;
        v00 ^= sgn_perm0;
        v01 ^= sgn_perm0;
        v02 ^= sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[0]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[1]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[2]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[3]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[4]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 32)) & benes_mask[5]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v02 ^ (v02 >> 8)) & benes_mask[6]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v02 ^ (v02 >> 16)) & benes_mask[7]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v02 ^ (v02 >> 32)) & benes_mask[8]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ v01) & benes_mask[9]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ v02) & benes_mask[10]; 
        v00 ^=  sgn_perm0;  v02 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ v01) & benes_mask[11]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[12]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[13]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[14]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 32)) & benes_mask[15]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[16]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[17]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v02 ^ (v02 >> 32)) & benes_mask[18]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v02 ^ (v02 >> 16)) & benes_mask[19]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v02 ^ (v02 >> 8)) & benes_mask[20]; 
        v02 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        // Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 0)[0] = v00 ;
(p_dest + 0)[1] = v01 ;
(p_dest + 0)[2] = v02 ;
        sgn_perm1 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v10, v11, v12)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm1 = (-(sgn_perm1 & 0x1ULL)) & 0xffffffffffffffffULL;
v10 ^= sgn_perm1;
v11 ^= sgn_perm1;
v12 ^= sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[0]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[1]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[2]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[3]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[4]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 32)) & benes_mask[5]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v12 ^ (v12 >> 8)) & benes_mask[6]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v12 ^ (v12 >> 16)) & benes_mask[7]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v12 ^ (v12 >> 32)) & benes_mask[8]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ v11) & benes_mask[9]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ v12) & benes_mask[10]; 
v10 ^=  sgn_perm1;  v12 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ v11) & benes_mask[11]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[12]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[13]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[14]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 32)) & benes_mask[15]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[16]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[17]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v12 ^ (v12 >> 32)) & benes_mask[18]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v12 ^ (v12 >> 16)) & benes_mask[19]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v12 ^ (v12 >> 8)) & benes_mask[20]; 
v12 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 4)[0] = v10 ;
(p_dest + 4)[1] = v11 ;
(p_dest + 4)[2] = v12 ;
        sgn_perm2 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v20, v21, v22)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm2 = (-(sgn_perm2 & 0x1ULL)) & 0xffffffffffffffffULL;
v20 ^= sgn_perm2;
v21 ^= sgn_perm2;
v22 ^= sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[0]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[1]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[2]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[3]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[4]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 32)) & benes_mask[5]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v22 ^ (v22 >> 8)) & benes_mask[6]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v22 ^ (v22 >> 16)) & benes_mask[7]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v22 ^ (v22 >> 32)) & benes_mask[8]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ v21) & benes_mask[9]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ v22) & benes_mask[10]; 
v20 ^=  sgn_perm2;  v22 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ v21) & benes_mask[11]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[12]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[13]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[14]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 32)) & benes_mask[15]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[16]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[17]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v22 ^ (v22 >> 32)) & benes_mask[18]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v22 ^ (v22 >> 16)) & benes_mask[19]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v22 ^ (v22 >> 8)) & benes_mask[20]; 
v22 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 8)[0] = v20 ;
(p_dest + 8)[1] = v21 ;
(p_dest + 8)[2] = v22 ;
        sgn_perm3 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v30, v31, v32)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm3 = (-(sgn_perm3 & 0x1ULL)) & 0xffffffffffffffffULL;
v30 ^= sgn_perm3;
v31 ^= sgn_perm3;
v32 ^= sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[0]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[1]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[2]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[3]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[4]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 32)) & benes_mask[5]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v32 ^ (v32 >> 8)) & benes_mask[6]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v32 ^ (v32 >> 16)) & benes_mask[7]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v32 ^ (v32 >> 32)) & benes_mask[8]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ v31) & benes_mask[9]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ v32) & benes_mask[10]; 
v30 ^=  sgn_perm3;  v32 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ v31) & benes_mask[11]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[12]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[13]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[14]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 32)) & benes_mask[15]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[16]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[17]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v32 ^ (v32 >> 32)) & benes_mask[18]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v32 ^ (v32 >> 16)) & benes_mask[19]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v32 ^ (v32 >> 8)) & benes_mask[20]; 
v32 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 12)[0] = v30 ;
(p_dest + 12)[1] = v31 ;
(p_dest + 12)[2] = v32 ;

        p_perm += 4;
        p_dest += 16;
        }
}


static void pi24_72(
   uint_mmv_t * p_src,
   uint16_t * p_perm,
   uint_mmv_t * benes_mask,
   uint_mmv_t * p_dest
)
{
    uint_fast32_t i1;
    for (i1 = 0; i1 < 72; ++i1) {
        uint_mmv_t sgn_perm = p_perm[i1];
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 2);
        // The following mask is used by the actual permutation code
        // %%PERM24_BENES_DECLARE "v"
uint_mmv_t v0, v1, v2;

        sgn_perm >>= 15;  // sign for permutation
        // Load 'ps' to temporary variables v0,...
        // %%PERM24_BENES_LOAD ps
v0 = (ps)[0];
v1 = (ps)[1];
v2 = (ps)[2];
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm
// Permute the 24 small integers in '(v0, v1, v2)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm = (-(sgn_perm & 0x1ULL)) & 0xffffffffffffffffULL;
v0 ^= sgn_perm;
v1 ^= sgn_perm;
v2 ^= sgn_perm;
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[0]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[1]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[2]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[3]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[4]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 32)) & benes_mask[5]; 
v1 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v2 ^ (v2 >> 8)) & benes_mask[6]; 
v2 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v2 ^ (v2 >> 16)) & benes_mask[7]; 
v2 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v2 ^ (v2 >> 32)) & benes_mask[8]; 
v2 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ v1) & benes_mask[9]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ v2) & benes_mask[10]; 
v0 ^=  sgn_perm;  v2 ^=  sgn_perm;
sgn_perm = (v0 ^ v1) & benes_mask[11]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[12]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[13]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[14]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 32)) & benes_mask[15]; 
v1 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[16]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[17]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v2 ^ (v2 >> 32)) & benes_mask[18]; 
v2 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v2 ^ (v2 >> 16)) & benes_mask[19]; 
v2 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v2 ^ (v2 >> 8)) & benes_mask[20]; 
v2 ^=  sgn_perm ^ (sgn_perm << 8);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE p_dest
(p_dest)[0] = v0 ;
(p_dest)[1] = v1 ;
(p_dest)[2] = v2 ;
        p_dest +=  4;      
        }
}

// %%END IF







// %%EXPORT
void mm_op255_do_pi(uint_mmv_t *v_in, mm_sub_op_pi_type *p_op, uint_mmv_t * v_out)
{
    uint_fast32_t i;
    uint_mmv_t *a_src[3], *a_dest[3];
    uint16_t *p_perm = p_op->tbl_perm24_big;

    // %%IF PERM24_USE_BENES_NET
    uint_mmv_t small_perm[21]; 

    // Prepare mask array from Benes network
    // %%PERM24_BENES_PREPARE "p_op->benes_net", small_perm
{
    uint_mmv_t tmp; 
    uint_fast8_t i;
    static uint8_t tbl[] = {
        // %%TABLE table_prepare_perm24, uint8_t
    0x00,0x01,0x02,0x10,0x11,0x12,0x20,0x21,
    0x22,0x03,0x04,0x05,0x06,0x07,0x08,0x16,
    0x17,0x18,0x26,0x27,0x28
    };

    for(i = 0; i < 21; ++i) {
        tmp = tbl[i];
        tmp = (p_op->benes_net)[tmp & 15] >> ((tmp & 0xf0) >> 1);
        // %%MMV_UINT_SPREAD tmp, tmp
        // Spread bits 0,...,7 of tmp to the (8-bit long) fields
        // of tmp. A field of tmp is set to 0xff if its 
        // corresponding bit in input tmp is one and to 0 otherwise.
        tmp = (tmp & 0xfULL) + ((tmp & 0xf0ULL) << 28);
        tmp = (tmp & 0x300000003ULL) 
            +  ((tmp & 0xc0000000cULL) << 14);
        tmp = (tmp & 0x1000100010001ULL) 
            +  ((tmp & 0x2000200020002ULL) << 7);
        tmp *= 255;
        // Bit spreading done.
        small_perm[i] = tmp;
    }
}
    // %%END IF
    
    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    a_src[0] = v_in + MM_OP255_OFS_X;
    a_dest[0] = v_out + MM_OP255_OFS_X;
    a_src[1] = v_in + MM_OP255_OFS_Z;
    a_src[2] = v_in + MM_OP255_OFS_Y;
    if (p_op->d & 0x800) {
        a_dest[1] = v_out + MM_OP255_OFS_Y;
        a_dest[2] = v_out + MM_OP255_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP255_OFS_Z;
        a_dest[2] = v_out + MM_OP255_OFS_Y;
    }

    for (i = 0; i < 3; ++i) 
        pi24_2048(a_src[i], p_perm, small_perm, i + 12, a_dest[i]);
    pi24_72(v_in, p_perm + 2048, small_perm, v_out);


    // Step 2: do rows with 64 entries // TODO: comment properly!!!!
    {
        // TODO: check this !!!!!!!!!!!!
        mm_sub_op_pi64_type *p_perm = p_op->tbl_perm64;
        uint8_t bytes[64];
        uint_mmv_t *p_out = v_out + MM_OP255_OFS_T;
        uint_mmv_t *p_end = p_out + 759 * 8;
        v_in +=  MM_OP255_OFS_T;
        for (; p_out < p_end; p_out += 8) {
            {
               uint_mmv_t v = p_perm->preimage;
               uint_mmv_t *p_in = v_in + ((v & 0x3ff) << 3);
               // %%LOAD_PERM64 p_in, bytes, v
               uint_mmv_t r0;
               v = (-((v >> 12) & 1)) & 0xffffffffffffffffULL;
               r0 =  (p_in)[0] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[0] = r0 >> 0;
               (bytes)[1] = r0 >> 8;
               (bytes)[2] = r0 >> 16;
               (bytes)[3] = r0 >> 24;
               (bytes)[4] = r0 >> 32;
               (bytes)[5] = r0 >> 40;
               (bytes)[6] = r0 >> 48;
               (bytes)[7] = r0 >> 56;
               r0 =  (p_in)[1] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[8] = r0 >> 0;
               (bytes)[9] = r0 >> 8;
               (bytes)[10] = r0 >> 16;
               (bytes)[11] = r0 >> 24;
               (bytes)[12] = r0 >> 32;
               (bytes)[13] = r0 >> 40;
               (bytes)[14] = r0 >> 48;
               (bytes)[15] = r0 >> 56;
               r0 =  (p_in)[2] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[16] = r0 >> 0;
               (bytes)[17] = r0 >> 8;
               (bytes)[18] = r0 >> 16;
               (bytes)[19] = r0 >> 24;
               (bytes)[20] = r0 >> 32;
               (bytes)[21] = r0 >> 40;
               (bytes)[22] = r0 >> 48;
               (bytes)[23] = r0 >> 56;
               r0 =  (p_in)[3] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[24] = r0 >> 0;
               (bytes)[25] = r0 >> 8;
               (bytes)[26] = r0 >> 16;
               (bytes)[27] = r0 >> 24;
               (bytes)[28] = r0 >> 32;
               (bytes)[29] = r0 >> 40;
               (bytes)[30] = r0 >> 48;
               (bytes)[31] = r0 >> 56;
               r0 =  (p_in)[4] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[32] = r0 >> 0;
               (bytes)[33] = r0 >> 8;
               (bytes)[34] = r0 >> 16;
               (bytes)[35] = r0 >> 24;
               (bytes)[36] = r0 >> 32;
               (bytes)[37] = r0 >> 40;
               (bytes)[38] = r0 >> 48;
               (bytes)[39] = r0 >> 56;
               r0 =  (p_in)[5] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[40] = r0 >> 0;
               (bytes)[41] = r0 >> 8;
               (bytes)[42] = r0 >> 16;
               (bytes)[43] = r0 >> 24;
               (bytes)[44] = r0 >> 32;
               (bytes)[45] = r0 >> 40;
               (bytes)[46] = r0 >> 48;
               (bytes)[47] = r0 >> 56;
               r0 =  (p_in)[6] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[48] = r0 >> 0;
               (bytes)[49] = r0 >> 8;
               (bytes)[50] = r0 >> 16;
               (bytes)[51] = r0 >> 24;
               (bytes)[52] = r0 >> 32;
               (bytes)[53] = r0 >> 40;
               (bytes)[54] = r0 >> 48;
               (bytes)[55] = r0 >> 56;
               r0 =  (p_in)[7] ^ (v);
               r0 &= 0xffffffffffffffffULL;
               (bytes)[56] = r0 >> 0;
               (bytes)[57] = r0 >> 8;
               (bytes)[58] = r0 >> 16;
               (bytes)[59] = r0 >> 24;
               (bytes)[60] = r0 >> 32;
               (bytes)[61] = r0 >> 40;
               (bytes)[62] = r0 >> 48;
               (bytes)[63] = r0 >> 56;
            }
            {
               // %%STORE_PERM64 bytes, p_out, "(p_perm->perm)"
               uint_mmv_t v;
               uint_fast8_t ri, r0, r1, r2;
               r0 = (p_perm->perm)[0];
               r1 = (p_perm->perm)[1];
               r2 = (p_perm->perm)[2];
               ri = r0;
               v = (uint_mmv_t)(bytes[0]) << 0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[0] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[1] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[2] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[3] = v ;
               ri ^= (p_perm->perm)[5];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[4] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[5] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[6] = v ;
               ri ^= (p_perm->perm)[3];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               p_out[7] = v ;
            }
            ++p_perm;
        } 
    }

    // If d is odd: negate some entries    
    if (p_op->d & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP255_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
            v[0] ^= 0xffffffffffff00ULL;
            v[1] ^= 0xff00ffffffULL;
            v[2] ^= 0xff00ffffffULL;
            v[3] ^= 0xff000000000000ffULL;
            v[4] ^= 0xff00ffffffULL;
            v[5] ^= 0xff000000000000ffULL;
            v[6] ^= 0xff000000000000ffULL;
            v[7] ^= 0xffffff00ff000000ULL;
            v += 8;
        }

        mm255_neg_scalprod_d_i(v); 
    }
} 





// %%EXPORT p
void mm_op255_pi(uint_mmv_t *v_in, uint32_t delta, uint32_t pi, uint_mmv_t * v_out)
{
    mm_sub_op_pi_type s_op;
    mm_sub_prep_pi(delta, pi, &s_op);
    mm_op255_do_pi(v_in, &s_op, v_out);
}


// %%EXPORT p
void mm_op255_delta(uint_mmv_t *v_in, uint32_t delta, uint_mmv_t * v_out)
{
    uint_fast32_t i, i1;
    uint8_t signs[2048];
    uint_mmv_t *a_src[3], *a_dest[3];

    mat24_op_all_cocode(delta, signs);
    for (i = 0; i < 72; ++i) signs[i] &= 7;
    for (i = 48; i < 72; ++i) signs[i] |= (delta & 0x800) >> (11 - 3);

    a_src[0] = v_in + MM_OP255_OFS_X;
    a_dest[0] = v_out + MM_OP255_OFS_X;
    a_src[1] = v_in + MM_OP255_OFS_Z;
    a_src[2] = v_in + MM_OP255_OFS_Y;
    if (delta & 0x800) {
        a_dest[1] = v_out + MM_OP255_OFS_Y;
        a_dest[2] = v_out + MM_OP255_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP255_OFS_Z;
        a_dest[2] = v_out + MM_OP255_OFS_Y;
    }

    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    for (i = 0; i < 3; ++i)  {
        for (i1 = 0; i1 < 2048; ++i1) {
            uint_mmv_t *p_src = a_src[i] + (i1 << 2);
            uint_mmv_t *p_dest = a_dest[i] + (i1 << 2);
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0xffffffffffffffffULL;
            p_dest[0] = p_src[0]  ^ sgn;
            p_dest[1] = p_src[1]  ^ sgn;
            p_dest[2] = p_src[2]  ^ sgn;
            // %%END FOR
            p_dest[3] = 0;
        }        
    }    

    {
        uint_mmv_t *p_src = v_in + MM_OP255_OFS_A;
        uint_mmv_t *p_dest = v_out + MM_OP255_OFS_A;
        for (i1 = 0; i1 < 72; ++i1) {
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0xffffffffffffffffULL;
            p_dest[0] = p_src[0]  ^ sgn;
            p_dest[1] = p_src[1]  ^ sgn;
            p_dest[2] = p_src[2]  ^ sgn;
            // %%END FOR
            p_dest[3] = 0;
            p_src +=  4;      
            p_dest +=  4;      
        }        
    }    


    // Step 2: do rows with 64 entries 
    // TODO: comment properly!!!!
    {
        v_in +=  MM_OP255_OFS_T;
        v_out += MM_OP255_OFS_T;
        for (i = 0; i < 759; ++i) {
            uint_mmv_t sign = mat24_def_octad_to_gcode(i) & delta;
            sign ^=  sign >> 6; sign ^=  sign >> 3;
            sign = -((0x96 >> (sign & 7)) & 1);
            sign &= 0xffffffffffffffffULL;
            // %%FOR i in range({V64_INTS})
            v_out[0] = v_in[0]  ^  sign;
            v_out[1] = v_in[1]  ^  sign;
            v_out[2] = v_in[2]  ^  sign;
            v_out[3] = v_in[3]  ^  sign;
            v_out[4] = v_in[4]  ^  sign;
            v_out[5] = v_in[5]  ^  sign;
            v_out[6] = v_in[6]  ^  sign;
            v_out[7] = v_in[7]  ^  sign;
            // %%END FOR
            v_in += 8;
            v_out += 8;
        } 
        v_out -= 759 * 8 +  MM_OP255_OFS_T; // restore v_out
    }

    // If d is odd: negate some entries    
    if (delta & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP255_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
v[0] ^= 0xffffffffffff00ULL;
v[1] ^= 0xff00ffffffULL;
v[2] ^= 0xff00ffffffULL;
v[3] ^= 0xff000000000000ffULL;
v[4] ^= 0xff00ffffffULL;
v[5] ^= 0xff000000000000ffULL;
v[6] ^= 0xff000000000000ffULL;
v[7] ^= 0xffffff00ff000000ULL;
            v += 8;
        }

        mm255_neg_scalprod_d_i(v); 
    }
}


