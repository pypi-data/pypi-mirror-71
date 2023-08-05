/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


// %%COMMENT
// TODO: Adjust this to new order of basis vectors rep!!!

#include <string.h>
#include "mm_op7.h"   




   
static const uint_mmv_t MM7_TBL_SCALPROD_HIGH[] = { 
// %%TABLE MMV_TBL_SCALPROD_HIGH, uint{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x7700000077000000ULL,0x0000000007707070ULL,
0x7070000070700000ULL,0x0000000077000770ULL,
0x0770000007700000ULL,0x0000000070707700ULL,
0x7700000000007700ULL,0x0000000070700770ULL,
0x0000000077007700ULL,0x0000000077007700ULL,
0x0770000070707700ULL,0x0000000007700000ULL,
0x7070000007707700ULL,0x0000000000007070ULL,
0x7070000000007070ULL,0x0000000007707700ULL,
0x0770000077007070ULL,0x0000000000000770ULL,
0x0000000070707070ULL,0x0000000070707070ULL,
0x7700000007707070ULL,0x0000000077000000ULL,
0x0770000000000770ULL,0x0000000077007070ULL,
0x7070000077000770ULL,0x0000000070700000ULL,
0x7700000070700770ULL,0x0000000000007700ULL,
0x0000000007700770ULL,0x0000000007700770ULL,
0x0007000700077770ULL,0x0000000000070007ULL,
0x7707000777077770ULL,0x0000000007777077ULL,
0x7077000770777770ULL,0x0000000077070777ULL,
0x0777000707777770ULL,0x0000000070777707ULL,
0x7707000700070070ULL,0x0000000070770777ULL,
0x0007000777070070ULL,0x0000000077077707ULL,
0x0777000770770070ULL,0x0000000007770007ULL,
0x7077000707770070ULL,0x0000000000077077ULL,
0x7077000700070700ULL,0x0000000007777707ULL,
0x0777000777070700ULL,0x0000000000070777ULL,
0x0007000770770700ULL,0x0000000070777077ULL,
0x7707000707770700ULL,0x0000000077070007ULL,
0x0777000700077000ULL,0x0000000077077077ULL,
0x7077000777077000ULL,0x0000000070770007ULL,
0x7707000770777000ULL,0x0000000000077707ULL,
0x0007000707777000ULL,0x0000000007770777ULL
};

static const uint_mmv_t MM7_TBL_SCALPROD_LOW[] = { 
// %%TABLE MMV_TBL_SCALPROD_LOW, uint{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x7777777777770000ULL,0x0000000077770000ULL,
0x7777777777770000ULL,0x0000000000007777ULL,
0x0000000000000000ULL,0x0000000077777777ULL,
0x7700770000000000ULL,0x0000000077007700ULL,
0x0077007777770000ULL,0x0000000000777700ULL,
0x0077007777770000ULL,0x0000000077000077ULL,
0x7700770000000000ULL,0x0000000000770077ULL,
0x7070707000000000ULL,0x0000000070707070ULL,
0x0707070777770000ULL,0x0000000007077070ULL,
0x0707070777770000ULL,0x0000000070700707ULL,
0x7070707000000000ULL,0x0000000007070707ULL,
0x0770077000000000ULL,0x0000000007700770ULL,
0x7007700777770000ULL,0x0000000070070770ULL,
0x7007700777770000ULL,0x0000000007707007ULL,
0x0770077000000000ULL,0x0000000070077007ULL
};




// %%EXPORT
void mm7_neg_scalprod_d_i(uint_mmv_t* v)
// negate entries d (x) i with sclar product equal to 1
{
    const uint_mmv_t* p0 = MM7_TBL_SCALPROD_HIGH;
    const uint_mmv_t* p0_end = p0 + 32 * 2;

    // inversion of entries (d (x) i) with scalar product 1
    for (; p0 < p0_end; p0 += 2) {
        const uint_mmv_t* p1 = MM7_TBL_SCALPROD_LOW;
        const uint_mmv_t* p1_end = p1 + 16 * 2;
        for (; p1 < p1_end; p1 += 2) {
            // %%SCALAR_PROD_2048_UNROLL p0, p1, v 
            uint_mmv_t v_t;
            v[0] ^= (v_t = p0[0] ^ p1[0]);
            v[2] ^= v_t ^ 0x7777000077770000ULL;
            v[4] ^= v_t ^ 0x777777770000ULL;
            v[6] ^= v_t ^ 0x7777777700000000ULL;
            v[1] ^= (v_t = p0[1] ^ p1[1]);
            v[3] ^= v_t ^ 0x77777777ULL;
            v[5] ^= v_t ^ 0x77777777ULL;
            v[7] ^= v_t ^ 0x0ULL;
            v +=   4 * 2;
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
        uint_mmv_t *ps0 = p_src + ((sgn_perm0 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v00, v01;
        uint_mmv_t sgn_perm1 = p_perm[1];
        uint_mmv_t *ps1 = p_src + ((sgn_perm1 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v10, v11;
        uint_mmv_t sgn_perm2 = p_perm[2];
        uint_mmv_t *ps2 = p_src + ((sgn_perm2 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v20, v21;
        uint_mmv_t sgn_perm3 = p_perm[3];
        uint_mmv_t *ps3 = p_src + ((sgn_perm3 & 0x7ff) << 1);
        // %%PERM24_BENES_DECLARE "v{i}"
        uint_mmv_t v30, v31;

        // Load 'ps' to temporary variables v00,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v00 = (ps0)[0];
        v01 = (ps0)[1];
        // Load 'ps' to temporary variables v10,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v10 = (ps1)[0];
        v11 = (ps1)[1];
        // Load 'ps' to temporary variables v20,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v20 = (ps2)[0];
        v21 = (ps2)[1];
        // Load 'ps' to temporary variables v30,...
        // %%PERM24_BENES_LOAD ps{i}, v{i}
        v30 = (ps3)[0];
        v31 = (ps3)[1];

        sgn_perm0 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
        // Permute the 24 small integers in '(v00, v01)' 
        // using the Benes network given by 'benes_mask'. All small   
        // integers are negated if bit 0 of 'sign' is set.
        sgn_perm0 = (-(sgn_perm0 & 0x1ULL)) & 0x7777777777777777ULL;
        v00 ^= sgn_perm0;
        sgn_perm0 &= 0x77777777ULL;
        v01 ^= sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 4)) & benes_mask[0]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[1]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[2]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[3]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v01 ^ (v01 >> 4)) & benes_mask[4]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[5]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[6]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ v01) & benes_mask[7]; 
        v00 ^=  sgn_perm0;  v01 ^=  sgn_perm0;
        sgn_perm0 = (v00 ^ (v00 >> 32)) & benes_mask[8]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 32);
        sgn_perm0 = (v00 ^ (v00 >> 16)) & benes_mask[9]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v00 ^ (v00 >> 8)) & benes_mask[10]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v00 ^ (v00 >> 4)) & benes_mask[11]; 
        v00 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        sgn_perm0 = (v01 ^ (v01 >> 16)) & benes_mask[12]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 16);
        sgn_perm0 = (v01 ^ (v01 >> 8)) & benes_mask[13]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 8);
        sgn_perm0 = (v01 ^ (v01 >> 4)) & benes_mask[14]; 
        v01 ^=  sgn_perm0 ^ (sgn_perm0 << 4);
        // Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 0)[0] = v00 ;
(p_dest + 0)[1] = v01 ;
        sgn_perm1 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v10, v11)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm1 = (-(sgn_perm1 & 0x1ULL)) & 0x7777777777777777ULL;
v10 ^= sgn_perm1;
sgn_perm1 &= 0x77777777ULL;
v11 ^= sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 4)) & benes_mask[0]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[1]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[2]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[3]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v11 ^ (v11 >> 4)) & benes_mask[4]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[5]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[6]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ v11) & benes_mask[7]; 
v10 ^=  sgn_perm1;  v11 ^=  sgn_perm1;
sgn_perm1 = (v10 ^ (v10 >> 32)) & benes_mask[8]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 32);
sgn_perm1 = (v10 ^ (v10 >> 16)) & benes_mask[9]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v10 ^ (v10 >> 8)) & benes_mask[10]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v10 ^ (v10 >> 4)) & benes_mask[11]; 
v10 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
sgn_perm1 = (v11 ^ (v11 >> 16)) & benes_mask[12]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 16);
sgn_perm1 = (v11 ^ (v11 >> 8)) & benes_mask[13]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 8);
sgn_perm1 = (v11 ^ (v11 >> 4)) & benes_mask[14]; 
v11 ^=  sgn_perm1 ^ (sgn_perm1 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 2)[0] = v10 ;
(p_dest + 2)[1] = v11 ;
        sgn_perm2 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v20, v21)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm2 = (-(sgn_perm2 & 0x1ULL)) & 0x7777777777777777ULL;
v20 ^= sgn_perm2;
sgn_perm2 &= 0x77777777ULL;
v21 ^= sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 4)) & benes_mask[0]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[1]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[2]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[3]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v21 ^ (v21 >> 4)) & benes_mask[4]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[5]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[6]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ v21) & benes_mask[7]; 
v20 ^=  sgn_perm2;  v21 ^=  sgn_perm2;
sgn_perm2 = (v20 ^ (v20 >> 32)) & benes_mask[8]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 32);
sgn_perm2 = (v20 ^ (v20 >> 16)) & benes_mask[9]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v20 ^ (v20 >> 8)) & benes_mask[10]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v20 ^ (v20 >> 4)) & benes_mask[11]; 
v20 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
sgn_perm2 = (v21 ^ (v21 >> 16)) & benes_mask[12]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 16);
sgn_perm2 = (v21 ^ (v21 >> 8)) & benes_mask[13]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 8);
sgn_perm2 = (v21 ^ (v21 >> 4)) & benes_mask[14]; 
v21 ^=  sgn_perm2 ^ (sgn_perm2 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 4)[0] = v20 ;
(p_dest + 4)[1] = v21 ;
        sgn_perm3 >>= sign_shift;  // sign for permutation
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm{i}, v{i}
// Permute the 24 small integers in '(v30, v31)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm3 = (-(sgn_perm3 & 0x1ULL)) & 0x7777777777777777ULL;
v30 ^= sgn_perm3;
sgn_perm3 &= 0x77777777ULL;
v31 ^= sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 4)) & benes_mask[0]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[1]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[2]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[3]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v31 ^ (v31 >> 4)) & benes_mask[4]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[5]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[6]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ v31) & benes_mask[7]; 
v30 ^=  sgn_perm3;  v31 ^=  sgn_perm3;
sgn_perm3 = (v30 ^ (v30 >> 32)) & benes_mask[8]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 32);
sgn_perm3 = (v30 ^ (v30 >> 16)) & benes_mask[9]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v30 ^ (v30 >> 8)) & benes_mask[10]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v30 ^ (v30 >> 4)) & benes_mask[11]; 
v30 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
sgn_perm3 = (v31 ^ (v31 >> 16)) & benes_mask[12]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 16);
sgn_perm3 = (v31 ^ (v31 >> 8)) & benes_mask[13]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 8);
sgn_perm3 = (v31 ^ (v31 >> 4)) & benes_mask[14]; 
v31 ^=  sgn_perm3 ^ (sgn_perm3 << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE "p_dest + {int: i * V24_INTS}", v{i}
(p_dest + 6)[0] = v30 ;
(p_dest + 6)[1] = v31 ;

        p_perm += 4;
        p_dest += 8;
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
        uint_mmv_t *ps = p_src + ((sgn_perm & 0x7ff) << 1);
        // The following mask is used by the actual permutation code
        // %%PERM24_BENES_DECLARE "v"
uint_mmv_t v0, v1;

        sgn_perm >>= 15;  // sign for permutation
        // Load 'ps' to temporary variables v0,...
        // %%PERM24_BENES_LOAD ps
v0 = (ps)[0];
v1 = (ps)[1];
        // Permute and possibly negate data in temp. variables
        // %%PERM24_BENES_PERMUTE benes_mask, sgn_perm
// Permute the 24 small integers in '(v0, v1)' 
// using the Benes network given by 'benes_mask'. All small   
// integers are negated if bit 0 of 'sign' is set.
sgn_perm = (-(sgn_perm & 0x1ULL)) & 0x7777777777777777ULL;
v0 ^= sgn_perm;
sgn_perm &= 0x77777777ULL;
v1 ^= sgn_perm;
sgn_perm = (v0 ^ (v0 >> 4)) & benes_mask[0]; 
v0 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[1]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[2]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[3]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v1 ^ (v1 >> 4)) & benes_mask[4]; 
v1 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[5]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[6]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ v1) & benes_mask[7]; 
v0 ^=  sgn_perm;  v1 ^=  sgn_perm;
sgn_perm = (v0 ^ (v0 >> 32)) & benes_mask[8]; 
v0 ^=  sgn_perm ^ (sgn_perm << 32);
sgn_perm = (v0 ^ (v0 >> 16)) & benes_mask[9]; 
v0 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v0 ^ (v0 >> 8)) & benes_mask[10]; 
v0 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v0 ^ (v0 >> 4)) & benes_mask[11]; 
v0 ^=  sgn_perm ^ (sgn_perm << 4);
sgn_perm = (v1 ^ (v1 >> 16)) & benes_mask[12]; 
v1 ^=  sgn_perm ^ (sgn_perm << 16);
sgn_perm = (v1 ^ (v1 >> 8)) & benes_mask[13]; 
v1 ^=  sgn_perm ^ (sgn_perm << 8);
sgn_perm = (v1 ^ (v1 >> 4)) & benes_mask[14]; 
v1 ^=  sgn_perm ^ (sgn_perm << 4);
// Permutation of small integers done.
        // Store temporary variables to 'p_dest'
        // %%PERM24_BENES_STORE p_dest
(p_dest)[0] = v0 ;
(p_dest)[1] = v1 ;
        p_dest +=  2;      
        }
}

// %%END IF







// %%EXPORT
void mm_op7_do_pi(uint_mmv_t *v_in, mm_sub_op_pi_type *p_op, uint_mmv_t * v_out)
{
    uint_fast32_t i;
    uint_mmv_t *a_src[3], *a_dest[3];
    uint16_t *p_perm = p_op->tbl_perm24_big;

    // %%IF PERM24_USE_BENES_NET
    uint_mmv_t small_perm[15]; 

    // Prepare mask array from Benes network
    // %%PERM24_BENES_PREPARE "p_op->benes_net", small_perm
{
    uint_mmv_t tmp; 
    uint_fast8_t i;
    static uint8_t tbl[] = {
        // %%TABLE table_prepare_perm24, uint8_t
    0x00,0x01,0x02,0x03,0x10,0x11,0x12,0x04,
    0x05,0x06,0x07,0x08,0x16,0x17,0x18
    };

    for(i = 0; i < 15; ++i) {
        tmp = tbl[i]; tmp = (p_op->benes_net)[tmp & 15] >> (tmp & 0xf0);
        // %%MMV_UINT_SPREAD tmp, tmp
        // Spread bits 0,...,15 of tmp to the (4-bit long) fields
        // of tmp. A field of tmp is set to 0x7 if its 
        // corresponding bit in input tmp is one and to 0 otherwise.
        tmp = (tmp & 0xffULL) + ((tmp & 0xff00ULL) << 24);
        tmp = (tmp & 0xf0000000fULL) 
            +  ((tmp & 0xf0000000f0ULL) << 12);
        tmp = (tmp & 0x3000300030003ULL) 
            +  ((tmp & 0xc000c000c000cULL) << 6);
        tmp = (tmp & 0x101010101010101ULL) 
            +  ((tmp & 0x202020202020202ULL) << 3);
        tmp *= 7;
        // Bit spreading done.
        small_perm[i] = tmp;
    }
}
    // %%END IF
    
    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    a_src[0] = v_in + MM_OP7_OFS_X;
    a_dest[0] = v_out + MM_OP7_OFS_X;
    a_src[1] = v_in + MM_OP7_OFS_Z;
    a_src[2] = v_in + MM_OP7_OFS_Y;
    if (p_op->d & 0x800) {
        a_dest[1] = v_out + MM_OP7_OFS_Y;
        a_dest[2] = v_out + MM_OP7_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP7_OFS_Z;
        a_dest[2] = v_out + MM_OP7_OFS_Y;
    }

    for (i = 0; i < 3; ++i) 
        pi24_2048(a_src[i], p_perm, small_perm, i + 12, a_dest[i]);
    pi24_72(v_in, p_perm + 2048, small_perm, v_out);


    // Step 2: do rows with 64 entries // TODO: comment properly!!!!
    {
        // TODO: check this !!!!!!!!!!!!
        mm_sub_op_pi64_type *p_perm = p_op->tbl_perm64;
        uint8_t bytes[64];
        uint_mmv_t *p_out = v_out + MM_OP7_OFS_T;
        uint_mmv_t *p_end = p_out + 759 * 4;
        v_in +=  MM_OP7_OFS_T;
        for (; p_out < p_end; p_out += 4) {
            {
               uint_mmv_t v = p_perm->preimage;
               uint_mmv_t *p_in = v_in + ((v & 0x3ff) << 2);
               // %%LOAD_PERM64 p_in, bytes, v
               uint_mmv_t r0, r1;
               v = (-((v >> 12) & 1)) & 0x7777777777777777ULL;
               r0 =  (p_in)[0] ^ (v);
               r1 = (r0 >> 4) & 0x707070707070707ULL;
               r0 &= 0x707070707070707ULL;
               (bytes)[0] = r0 >> 0;
               (bytes)[1] = r1 >> 0;
               (bytes)[2] = r0 >> 8;
               (bytes)[3] = r1 >> 8;
               (bytes)[4] = r0 >> 16;
               (bytes)[5] = r1 >> 16;
               (bytes)[6] = r0 >> 24;
               (bytes)[7] = r1 >> 24;
               (bytes)[8] = r0 >> 32;
               (bytes)[9] = r1 >> 32;
               (bytes)[10] = r0 >> 40;
               (bytes)[11] = r1 >> 40;
               (bytes)[12] = r0 >> 48;
               (bytes)[13] = r1 >> 48;
               (bytes)[14] = r0 >> 56;
               (bytes)[15] = r1 >> 56;
               r0 =  (p_in)[1] ^ (v);
               r1 = (r0 >> 4) & 0x707070707070707ULL;
               r0 &= 0x707070707070707ULL;
               (bytes)[16] = r0 >> 0;
               (bytes)[17] = r1 >> 0;
               (bytes)[18] = r0 >> 8;
               (bytes)[19] = r1 >> 8;
               (bytes)[20] = r0 >> 16;
               (bytes)[21] = r1 >> 16;
               (bytes)[22] = r0 >> 24;
               (bytes)[23] = r1 >> 24;
               (bytes)[24] = r0 >> 32;
               (bytes)[25] = r1 >> 32;
               (bytes)[26] = r0 >> 40;
               (bytes)[27] = r1 >> 40;
               (bytes)[28] = r0 >> 48;
               (bytes)[29] = r1 >> 48;
               (bytes)[30] = r0 >> 56;
               (bytes)[31] = r1 >> 56;
               r0 =  (p_in)[2] ^ (v);
               r1 = (r0 >> 4) & 0x707070707070707ULL;
               r0 &= 0x707070707070707ULL;
               (bytes)[32] = r0 >> 0;
               (bytes)[33] = r1 >> 0;
               (bytes)[34] = r0 >> 8;
               (bytes)[35] = r1 >> 8;
               (bytes)[36] = r0 >> 16;
               (bytes)[37] = r1 >> 16;
               (bytes)[38] = r0 >> 24;
               (bytes)[39] = r1 >> 24;
               (bytes)[40] = r0 >> 32;
               (bytes)[41] = r1 >> 32;
               (bytes)[42] = r0 >> 40;
               (bytes)[43] = r1 >> 40;
               (bytes)[44] = r0 >> 48;
               (bytes)[45] = r1 >> 48;
               (bytes)[46] = r0 >> 56;
               (bytes)[47] = r1 >> 56;
               r0 =  (p_in)[3] ^ (v);
               r1 = (r0 >> 4) & 0x707070707070707ULL;
               r0 &= 0x707070707070707ULL;
               (bytes)[48] = r0 >> 0;
               (bytes)[49] = r1 >> 0;
               (bytes)[50] = r0 >> 8;
               (bytes)[51] = r1 >> 8;
               (bytes)[52] = r0 >> 16;
               (bytes)[53] = r1 >> 16;
               (bytes)[54] = r0 >> 24;
               (bytes)[55] = r1 >> 24;
               (bytes)[56] = r0 >> 32;
               (bytes)[57] = r1 >> 32;
               (bytes)[58] = r0 >> 40;
               (bytes)[59] = r1 >> 40;
               (bytes)[60] = r0 >> 48;
               (bytes)[61] = r1 >> 48;
               (bytes)[62] = r0 >> 56;
               (bytes)[63] = r1 >> 56;
            }
            {
               // %%STORE_PERM64 bytes, p_out, "(p_perm->perm)"
               uint_mmv_t v;
               uint_fast8_t ri, r0, r1, r2, r3;
               r0 = (p_perm->perm)[0];
               r1 = (p_perm->perm)[1];
               r2 = (p_perm->perm)[2];
               r3 = (p_perm->perm)[3];
               ri = r0;
               v = (uint_mmv_t)(bytes[0]) << 0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[0] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[1] = v ;
               ri ^= (p_perm->perm)[5];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[2] = v ;
               ri ^= (p_perm->perm)[4];
               v = (uint_mmv_t)(bytes[ri]) << 0;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 4;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 8;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 12;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 16;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 20;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 24;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 28;
               ri ^= r3;
               v += (uint_mmv_t)(bytes[ri]) << 32;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 36;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 40;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 44;
               ri ^= r2;
               v += (uint_mmv_t)(bytes[ri]) << 48;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 52;
               ri ^= r1;
               v += (uint_mmv_t)(bytes[ri]) << 56;
               ri ^= r0;
               v += (uint_mmv_t)(bytes[ri]) << 60;
               p_out[3] = v ;
            }
            ++p_perm;
        } 
    }

    // If d is odd: negate some entries    
    if (p_op->d & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP7_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
            v[0] ^= 0x7077707777770ULL;
            v[1] ^= 0x7000000700070777ULL;
            v[2] ^= 0x7000000700070777ULL;
            v[3] ^= 0x7770700070000007ULL;
            v += 4;
        }

        mm7_neg_scalprod_d_i(v); 
    }
} 





// %%EXPORT p
void mm_op7_pi(uint_mmv_t *v_in, uint32_t delta, uint32_t pi, uint_mmv_t * v_out)
{
    mm_sub_op_pi_type s_op;
    mm_sub_prep_pi(delta, pi, &s_op);
    mm_op7_do_pi(v_in, &s_op, v_out);
}


// %%EXPORT p
void mm_op7_delta(uint_mmv_t *v_in, uint32_t delta, uint_mmv_t * v_out)
{
    uint_fast32_t i, i1;
    uint8_t signs[2048];
    uint_mmv_t *a_src[3], *a_dest[3];

    mat24_op_all_cocode(delta, signs);
    for (i = 0; i < 72; ++i) signs[i] &= 7;
    for (i = 48; i < 72; ++i) signs[i] |= (delta & 0x800) >> (11 - 3);

    a_src[0] = v_in + MM_OP7_OFS_X;
    a_dest[0] = v_out + MM_OP7_OFS_X;
    a_src[1] = v_in + MM_OP7_OFS_Z;
    a_src[2] = v_in + MM_OP7_OFS_Y;
    if (delta & 0x800) {
        a_dest[1] = v_out + MM_OP7_OFS_Y;
        a_dest[2] = v_out + MM_OP7_OFS_Z;
    } else {
        a_dest[1] = v_out + MM_OP7_OFS_Z;
        a_dest[2] = v_out + MM_OP7_OFS_Y;
    }

    // Step 1: do rows with 24 entries 
    // TODO: comment properly!!!!
    for (i = 0; i < 3; ++i)  {
        for (i1 = 0; i1 < 2048; ++i1) {
            uint_mmv_t *p_src = a_src[i] + (i1 << 1);
            uint_mmv_t *p_dest = a_dest[i] + (i1 << 1);
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0x7777777777777777ULL;
            p_dest[0] = p_src[0]  ^ sgn;
            sgn &= 0x77777777ULL;
            p_dest[1] = p_src[1]  ^ sgn;
            // %%END FOR
        }        
    }    

    {
        uint_mmv_t *p_src = v_in + MM_OP7_OFS_A;
        uint_mmv_t *p_dest = v_out + MM_OP7_OFS_A;
        for (i1 = 0; i1 < 72; ++i1) {
            uint_mmv_t sgn = -((signs[i1] >> i) & 1);
            // %%FOR i in range(V24_INTS_USED)
            sgn &= 0x7777777777777777ULL;
            p_dest[0] = p_src[0]  ^ sgn;
            sgn &= 0x77777777ULL;
            p_dest[1] = p_src[1]  ^ sgn;
            // %%END FOR
            p_src +=  2;      
            p_dest +=  2;      
        }        
    }    


    // Step 2: do rows with 64 entries 
    // TODO: comment properly!!!!
    {
        v_in +=  MM_OP7_OFS_T;
        v_out += MM_OP7_OFS_T;
        for (i = 0; i < 759; ++i) {
            uint_mmv_t sign = mat24_def_octad_to_gcode(i) & delta;
            sign ^=  sign >> 6; sign ^=  sign >> 3;
            sign = -((0x96 >> (sign & 7)) & 1);
            sign &= 0x7777777777777777ULL;
            // %%FOR i in range({V64_INTS})
            v_out[0] = v_in[0]  ^  sign;
            v_out[1] = v_in[1]  ^  sign;
            v_out[2] = v_in[2]  ^  sign;
            v_out[3] = v_in[3]  ^  sign;
            // %%END FOR
            v_in += 4;
            v_out += 4;
        } 
        v_out -= 759 * 4 +  MM_OP7_OFS_T; // restore v_out
    }

    // If d is odd: negate some entries    
    if (delta & 0x800) {
        uint_fast16_t i;
        uint_mmv_t *v = v_out + MM_OP7_OFS_T;

        // Step odd 1:  negate suboctads of weight 4n+2 for tag T
        for (i = 0; i < 759; ++i) {
            // %%INVERT_PERM64 v
v[0] ^= 0x7077707777770ULL;
v[1] ^= 0x7000000700070777ULL;
v[2] ^= 0x7000000700070777ULL;
v[3] ^= 0x7770700070000007ULL;
            v += 4;
        }

        mm7_neg_scalprod_d_i(v); 
    }
}


