/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

// %%COMMENT
// TODO: Yet to be documented!!!


#include <string.h>
#include "mat24_functions.h"
#include "mm_op255.h"   


static void mm_op255_xi_mon(
    uint_mmv_t * v_in,  
    uint32_t exp1, 
    uint_mmv_t * v_out
)
{
    // Caution: this uses v_out[MM_OP255_OFS_Z:] as temporary storage
    uint_mmv_t *p_src, *p_dest;
    uint_fast32_t i, j;
    uint_fast32_t diff = exp1 ? 4096 : 0;
    uint8_t *b =  (uint8_t*)(v_out + MM_OP255_OFS_Z), *p_b;
    mm_sub_table_xi_type *p_tables = mm_sub_table_xi[exp1];
    uint16_t *p_perm;
    uint32_t *p_sign;



    ///////////////////////////////////////////////////////////////
    // Map tag BC to tag BC.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 96;
    p_dest = v_out + 96;
    p_sign = p_tables[0].p_sign;
    p_perm = p_tables[0].p_perm;

    for (i = 0; i < 1; ++i) {
        p_b = b;
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_LOAD p_src, p_b, {i_src.SHAPE[2]}
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[0] = r0 >> 0;
           (p_b)[1] = r0 >> 8;
           (p_b)[2] = r0 >> 16;
           (p_b)[3] = r0 >> 24;
           (p_b)[4] = r0 >> 32;
           (p_b)[5] = r0 >> 40;
           (p_b)[6] = r0 >> 48;
           (p_b)[7] = r0 >> 56;
           r0 =  (p_src)[1];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[8] = r0 >> 0;
           (p_b)[9] = r0 >> 8;
           (p_b)[10] = r0 >> 16;
           (p_b)[11] = r0 >> 24;
           (p_b)[12] = r0 >> 32;
           (p_b)[13] = r0 >> 40;
           (p_b)[14] = r0 >> 48;
           (p_b)[15] = r0 >> 56;
           r0 =  (p_src)[2];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[16] = r0 >> 0;
           (p_b)[17] = r0 >> 8;
           (p_b)[18] = r0 >> 16;
           (p_b)[19] = r0 >> 24;
           (p_b)[20] = r0 >> 32;
           (p_b)[21] = r0 >> 40;
           (p_b)[22] = r0 >> 48;
           (p_b)[23] = r0 >> 56;
           r0 =  (p_src)[3];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[24] = r0 >> 0;
           (p_b)[25] = r0 >> 8;
           (p_b)[26] = r0 >> 16;
           (p_b)[27] = r0 >> 24;
           (p_b)[28] = r0 >> 32;
           (p_b)[29] = r0 >> 40;
           (p_b)[30] = r0 >> 48;
           (p_b)[31] = r0 >> 56;
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, {i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T0 to tag T0.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 408;
    p_dest = v_out + 408;
    p_sign = p_tables[1].p_sign;
    p_perm = p_tables[1].p_perm;

    for (i = 0; i < 45; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, {i_src.SHAPE[2]}
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[0] = r0 >> 0;
           (p_b)[1] = r0 >> 8;
           (p_b)[2] = r0 >> 16;
           (p_b)[3] = r0 >> 24;
           (p_b)[4] = r0 >> 32;
           (p_b)[5] = r0 >> 40;
           (p_b)[6] = r0 >> 48;
           (p_b)[7] = r0 >> 56;
           r0 =  (p_src)[1];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[8] = r0 >> 0;
           (p_b)[9] = r0 >> 8;
           (p_b)[10] = r0 >> 16;
           (p_b)[11] = r0 >> 24;
           (p_b)[12] = r0 >> 32;
           (p_b)[13] = r0 >> 40;
           (p_b)[14] = r0 >> 48;
           (p_b)[15] = r0 >> 56;
           r0 =  (p_src)[2];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[16] = r0 >> 0;
           (p_b)[17] = r0 >> 8;
           (p_b)[18] = r0 >> 16;
           (p_b)[19] = r0 >> 24;
           (p_b)[20] = r0 >> 32;
           (p_b)[21] = r0 >> 40;
           (p_b)[22] = r0 >> 48;
           (p_b)[23] = r0 >> 56;
           r0 =  (p_src)[3];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[24] = r0 >> 0;
           (p_b)[25] = r0 >> 8;
           (p_b)[26] = r0 >> 16;
           (p_b)[27] = r0 >> 24;
           (p_b)[28] = r0 >> 32;
           (p_b)[29] = r0 >> 40;
           (p_b)[30] = r0 >> 48;
           (p_b)[31] = r0 >> 56;
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, {i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T1 to tag X0 if e = 1
    // Map tag T1 to tag X1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 3288;
    p_dest = v_out + 6360;
    p_dest += diff;
    p_sign = p_tables[2].p_sign;
    p_perm = p_tables[2].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_LOAD p_src, p_b, {i_src.SHAPE[2]}
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[0] = r0 >> 0;
           (p_b)[1] = r0 >> 8;
           (p_b)[2] = r0 >> 16;
           (p_b)[3] = r0 >> 24;
           (p_b)[4] = r0 >> 32;
           (p_b)[5] = r0 >> 40;
           (p_b)[6] = r0 >> 48;
           (p_b)[7] = r0 >> 56;
           r0 =  (p_src)[1];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[8] = r0 >> 0;
           (p_b)[9] = r0 >> 8;
           (p_b)[10] = r0 >> 16;
           (p_b)[11] = r0 >> 24;
           (p_b)[12] = r0 >> 32;
           (p_b)[13] = r0 >> 40;
           (p_b)[14] = r0 >> 48;
           (p_b)[15] = r0 >> 56;
           r0 =  (p_src)[2];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[16] = r0 >> 0;
           (p_b)[17] = r0 >> 8;
           (p_b)[18] = r0 >> 16;
           (p_b)[19] = r0 >> 24;
           (p_b)[20] = r0 >> 32;
           (p_b)[21] = r0 >> 40;
           (p_b)[22] = r0 >> 48;
           (p_b)[23] = r0 >> 56;
           r0 =  (p_src)[3];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[24] = r0 >> 0;
           (p_b)[25] = r0 >> 8;
           (p_b)[26] = r0 >> 16;
           (p_b)[27] = r0 >> 24;
           (p_b)[28] = r0 >> 32;
           (p_b)[29] = r0 >> 40;
           (p_b)[30] = r0 >> 48;
           (p_b)[31] = r0 >> 56;
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, {i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           p_dest[3] = 0;
           p_dest += 4;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X0 to tag X1 if e = 1
    // Map tag X1 to tag X0 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 6360;
    p_src += diff;
    p_dest = v_out + 10456;
    p_dest -= diff;
    p_sign = p_tables[3].p_sign;
    p_perm = p_tables[3].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, {i_src.SHAPE[2]}
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[0] = r0 >> 0;
           (p_b)[1] = r0 >> 8;
           (p_b)[2] = r0 >> 16;
           (p_b)[3] = r0 >> 24;
           (p_b)[4] = r0 >> 32;
           (p_b)[5] = r0 >> 40;
           (p_b)[6] = r0 >> 48;
           (p_b)[7] = r0 >> 56;
           r0 =  (p_src)[1];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[8] = r0 >> 0;
           (p_b)[9] = r0 >> 8;
           (p_b)[10] = r0 >> 16;
           (p_b)[11] = r0 >> 24;
           (p_b)[12] = r0 >> 32;
           (p_b)[13] = r0 >> 40;
           (p_b)[14] = r0 >> 48;
           (p_b)[15] = r0 >> 56;
           r0 =  (p_src)[2];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[16] = r0 >> 0;
           (p_b)[17] = r0 >> 8;
           (p_b)[18] = r0 >> 16;
           (p_b)[19] = r0 >> 24;
           (p_b)[20] = r0 >> 32;
           (p_b)[21] = r0 >> 40;
           (p_b)[22] = r0 >> 48;
           (p_b)[23] = r0 >> 56;
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, {i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           p_dest[3] = 0;
           p_dest += 4;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X1 to tag T1 if e = 1
    // Map tag X0 to tag T1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 10456;
    p_src -= diff;
    p_dest = v_out + 3288;
    p_sign = p_tables[4].p_sign;
    p_perm = p_tables[4].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, {i_src.SHAPE[2]}
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[0] = r0 >> 0;
           (p_b)[1] = r0 >> 8;
           (p_b)[2] = r0 >> 16;
           (p_b)[3] = r0 >> 24;
           (p_b)[4] = r0 >> 32;
           (p_b)[5] = r0 >> 40;
           (p_b)[6] = r0 >> 48;
           (p_b)[7] = r0 >> 56;
           r0 =  (p_src)[1];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[8] = r0 >> 0;
           (p_b)[9] = r0 >> 8;
           (p_b)[10] = r0 >> 16;
           (p_b)[11] = r0 >> 24;
           (p_b)[12] = r0 >> 32;
           (p_b)[13] = r0 >> 40;
           (p_b)[14] = r0 >> 48;
           (p_b)[15] = r0 >> 56;
           r0 =  (p_src)[2];
           r0 &= 0xffffffffffffffffULL;
           (p_b)[16] = r0 >> 0;
           (p_b)[17] = r0 >> 8;
           (p_b)[18] = r0 >> 16;
           (p_b)[19] = r0 >> 24;
           (p_b)[20] = r0 >> 32;
           (p_b)[21] = r0 >> 40;
           (p_b)[22] = r0 >> 48;
           (p_b)[23] = r0 >> 56;
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, {i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0xff if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 255;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }
}

static uint_mmv_t TAB255_XI64_MASK[] = {
// %%TABLE TABLE_MUL_MATRIX_XI64, uint{INT_BITS}
0x000000ff000000ffULL,0x0000000000000000ULL,
0x000000ff000000ffULL,0xffffffffffffffffULL,
0x0000000000000000ULL,0x000000ff000000ffULL,
0xffffffffffffffffULL,0x000000ff000000ffULL
};


#define HALF_YZ_SHIFT 12

static uint32_t TAB255_XI64_OFFSET[2][4] = {
    {
        MM_OP255_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
    {
        MM_OP255_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP255_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
};




static void mm_op255_xi_yz(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    uint_mmv_t *p_mask =  TAB255_XI64_MASK + exp1;
    for (i = 0; i < 64; ++i) {
        // %%MUL_MATRIX_XI64 v_in, p_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;
        uint_mmv_t r10, r11, r12, r13, r14;
        uint_mmv_t r15, r16, r17, r18, r19;
        uint_mmv_t r20, r21, r22, r23, r24;
        uint_mmv_t r25, r26, r27, r28, r29;
        uint_mmv_t r30, r31, r32;

        uint_fast32_t i;

        // TODO: write comment!!!
        // 
        for (i = 0; i < 3; ++i) {
        r0 = v_in[0] ^  p_mask[2];
        r16 = ((r0 ^ (r0 >> 8)) & 0xff000000ff00ULL);
        r0 ^= (r16 | (r16 << 8));
        r1 = v_in[56] ^  p_mask[0];
        r16 = ((r1 ^ (r1 >> 8)) & 0xff000000ff00ULL);
        r1 ^= (r16 | (r16 << 8));
        r2 = v_in[52] ^  p_mask[0];
        r16 = ((r2 ^ (r2 >> 8)) & 0xff000000ff00ULL);
        r2 ^= (r16 | (r16 << 8));
        r3 = v_in[12] ^  p_mask[0];
        r16 = ((r3 ^ (r3 >> 8)) & 0xff000000ff00ULL);
        r3 ^= (r16 | (r16 << 8));
        r4 = v_in[44] ^  p_mask[0];
        r16 = ((r4 ^ (r4 >> 8)) & 0xff000000ff00ULL);
        r4 ^= (r16 | (r16 << 8));
        r5 = v_in[20] ^  p_mask[0];
        r16 = ((r5 ^ (r5 >> 8)) & 0xff000000ff00ULL);
        r5 ^= (r16 | (r16 << 8));
        r6 = v_in[24] ^  p_mask[0];
        r16 = ((r6 ^ (r6 >> 8)) & 0xff000000ff00ULL);
        r6 ^= (r16 | (r16 << 8));
        r7 = v_in[32] ^  p_mask[2];
        r16 = ((r7 ^ (r7 >> 8)) & 0xff000000ff00ULL);
        r7 ^= (r16 | (r16 << 8));
        r8 = v_in[28] ^  p_mask[0];
        r16 = ((r8 ^ (r8 >> 8)) & 0xff000000ff00ULL);
        r8 ^= (r16 | (r16 << 8));
        r9 = v_in[36] ^  p_mask[0];
        r16 = ((r9 ^ (r9 >> 8)) & 0xff000000ff00ULL);
        r9 ^= (r16 | (r16 << 8));
        r10 = v_in[40] ^  p_mask[0];
        r16 = ((r10 ^ (r10 >> 8)) & 0xff000000ff00ULL);
        r10 ^= (r16 | (r16 << 8));
        r11 = v_in[16] ^  p_mask[2];
        r16 = ((r11 ^ (r11 >> 8)) & 0xff000000ff00ULL);
        r11 ^= (r16 | (r16 << 8));
        r12 = v_in[48] ^  p_mask[0];
        r16 = ((r12 ^ (r12 >> 8)) & 0xff000000ff00ULL);
        r12 ^= (r16 | (r16 << 8));
        r13 = v_in[8] ^  p_mask[2];
        r16 = ((r13 ^ (r13 >> 8)) & 0xff000000ff00ULL);
        r13 ^= (r16 | (r16 << 8));
        r14 = v_in[4] ^  p_mask[2];
        r16 = ((r14 ^ (r14 >> 8)) & 0xff000000ff00ULL);
        r14 ^= (r16 | (r16 << 8));
        r15 = v_in[60] ^  p_mask[2];
        r16 = ((r15 ^ (r15 >> 8)) & 0xff000000ff00ULL);
        r15 ^= (r16 | (r16 << 8));
        // Expansion for Hadamard operation:
        // There is no space for a carry bit between bit fields. So 
        // we move bit field 2*i + 1  to bit field 2*i + 128.
        r16 = ((r0 >> 8) & 0xff00ff00ff00ffULL);
        r0 = (r0 & 0xff00ff00ff00ffULL);
        r17 = ((r1 >> 8) & 0xff00ff00ff00ffULL);
        r1 = (r1 & 0xff00ff00ff00ffULL);
        r18 = ((r2 >> 8) & 0xff00ff00ff00ffULL);
        r2 = (r2 & 0xff00ff00ff00ffULL);
        r19 = ((r3 >> 8) & 0xff00ff00ff00ffULL);
        r3 = (r3 & 0xff00ff00ff00ffULL);
        r20 = ((r4 >> 8) & 0xff00ff00ff00ffULL);
        r4 = (r4 & 0xff00ff00ff00ffULL);
        r21 = ((r5 >> 8) & 0xff00ff00ff00ffULL);
        r5 = (r5 & 0xff00ff00ff00ffULL);
        r22 = ((r6 >> 8) & 0xff00ff00ff00ffULL);
        r6 = (r6 & 0xff00ff00ff00ffULL);
        r23 = ((r7 >> 8) & 0xff00ff00ff00ffULL);
        r7 = (r7 & 0xff00ff00ff00ffULL);
        r24 = ((r8 >> 8) & 0xff00ff00ff00ffULL);
        r8 = (r8 & 0xff00ff00ff00ffULL);
        r25 = ((r9 >> 8) & 0xff00ff00ff00ffULL);
        r9 = (r9 & 0xff00ff00ff00ffULL);
        r26 = ((r10 >> 8) & 0xff00ff00ff00ffULL);
        r10 = (r10 & 0xff00ff00ff00ffULL);
        r27 = ((r11 >> 8) & 0xff00ff00ff00ffULL);
        r11 = (r11 & 0xff00ff00ff00ffULL);
        r28 = ((r12 >> 8) & 0xff00ff00ff00ffULL);
        r12 = (r12 & 0xff00ff00ff00ffULL);
        r29 = ((r13 >> 8) & 0xff00ff00ff00ffULL);
        r13 = (r13 & 0xff00ff00ff00ffULL);
        r30 = ((r14 >> 8) & 0xff00ff00ff00ffULL);
        r14 = (r14 & 0xff00ff00ff00ffULL);
        r31 = ((r15 >> 8) & 0xff00ff00ff00ffULL);
        r15 = (r15 & 0xff00ff00ff00ffULL);
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r32 = (((r0 << 16) & 0xff000000ff0000ULL)
            | ((r0 & 0xff000000ff0000ULL) >> 16));
        r0 = ((r0 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (((r1 << 16) & 0xff000000ff0000ULL)
            | ((r1 & 0xff000000ff0000ULL) >> 16));
        r1 = ((r1 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r32) + (r32 >> 8));
        r32 = (((r2 << 16) & 0xff000000ff0000ULL)
            | ((r2 & 0xff000000ff0000ULL) >> 16));
        r2 = ((r2 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r32) + (r32 >> 8));
        r32 = (((r3 << 16) & 0xff000000ff0000ULL)
            | ((r3 & 0xff000000ff0000ULL) >> 16));
        r3 = ((r3 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r32) + (r32 >> 8));
        r32 = (((r4 << 16) & 0xff000000ff0000ULL)
            | ((r4 & 0xff000000ff0000ULL) >> 16));
        r4 = ((r4 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r32) + (r32 >> 8));
        r32 = (((r5 << 16) & 0xff000000ff0000ULL)
            | ((r5 & 0xff000000ff0000ULL) >> 16));
        r5 = ((r5 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r32) + (r32 >> 8));
        r32 = (((r6 << 16) & 0xff000000ff0000ULL)
            | ((r6 & 0xff000000ff0000ULL) >> 16));
        r6 = ((r6 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r32) + (r32 >> 8));
        r32 = (((r7 << 16) & 0xff000000ff0000ULL)
            | ((r7 & 0xff000000ff0000ULL) >> 16));
        r7 = ((r7 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r32) + (r32 >> 8));
        r32 = (((r8 << 16) & 0xff000000ff0000ULL)
            | ((r8 & 0xff000000ff0000ULL) >> 16));
        r8 = ((r8 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r32) + (r32 >> 8));
        r32 = (((r9 << 16) & 0xff000000ff0000ULL)
            | ((r9 & 0xff000000ff0000ULL) >> 16));
        r9 = ((r9 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r32) + (r32 >> 8));
        r32 = (((r10 << 16) & 0xff000000ff0000ULL)
            | ((r10 & 0xff000000ff0000ULL) >> 16));
        r10 = ((r10 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r32) + (r32 >> 8));
        r32 = (((r11 << 16) & 0xff000000ff0000ULL)
            | ((r11 & 0xff000000ff0000ULL) >> 16));
        r11 = ((r11 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r32) + (r32 >> 8));
        r32 = (((r12 << 16) & 0xff000000ff0000ULL)
            | ((r12 & 0xff000000ff0000ULL) >> 16));
        r12 = ((r12 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r32) + (r32 >> 8));
        r32 = (((r13 << 16) & 0xff000000ff0000ULL)
            | ((r13 & 0xff000000ff0000ULL) >> 16));
        r13 = ((r13 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r32) + (r32 >> 8));
        r32 = (((r14 << 16) & 0xff000000ff0000ULL)
            | ((r14 & 0xff000000ff0000ULL) >> 16));
        r14 = ((r14 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r32) + (r32 >> 8));
        r32 = (((r15 << 16) & 0xff000000ff0000ULL)
            | ((r15 & 0xff000000ff0000ULL) >> 16));
        r15 = ((r15 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r32) + (r32 >> 8));
        r32 = (((r16 << 16) & 0xff000000ff0000ULL)
            | ((r16 & 0xff000000ff0000ULL) >> 16));
        r16 = ((r16 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r16 & 0x100010001000100ULL);
        r16 = ((r16 - r32) + (r32 >> 8));
        r32 = (((r17 << 16) & 0xff000000ff0000ULL)
            | ((r17 & 0xff000000ff0000ULL) >> 16));
        r17 = ((r17 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r17 & 0x100010001000100ULL);
        r17 = ((r17 - r32) + (r32 >> 8));
        r32 = (((r18 << 16) & 0xff000000ff0000ULL)
            | ((r18 & 0xff000000ff0000ULL) >> 16));
        r18 = ((r18 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r18 & 0x100010001000100ULL);
        r18 = ((r18 - r32) + (r32 >> 8));
        r32 = (((r19 << 16) & 0xff000000ff0000ULL)
            | ((r19 & 0xff000000ff0000ULL) >> 16));
        r19 = ((r19 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r19 & 0x100010001000100ULL);
        r19 = ((r19 - r32) + (r32 >> 8));
        r32 = (((r20 << 16) & 0xff000000ff0000ULL)
            | ((r20 & 0xff000000ff0000ULL) >> 16));
        r20 = ((r20 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r20 & 0x100010001000100ULL);
        r20 = ((r20 - r32) + (r32 >> 8));
        r32 = (((r21 << 16) & 0xff000000ff0000ULL)
            | ((r21 & 0xff000000ff0000ULL) >> 16));
        r21 = ((r21 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r21 & 0x100010001000100ULL);
        r21 = ((r21 - r32) + (r32 >> 8));
        r32 = (((r22 << 16) & 0xff000000ff0000ULL)
            | ((r22 & 0xff000000ff0000ULL) >> 16));
        r22 = ((r22 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r22 & 0x100010001000100ULL);
        r22 = ((r22 - r32) + (r32 >> 8));
        r32 = (((r23 << 16) & 0xff000000ff0000ULL)
            | ((r23 & 0xff000000ff0000ULL) >> 16));
        r23 = ((r23 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r23 & 0x100010001000100ULL);
        r23 = ((r23 - r32) + (r32 >> 8));
        r32 = (((r24 << 16) & 0xff000000ff0000ULL)
            | ((r24 & 0xff000000ff0000ULL) >> 16));
        r24 = ((r24 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r24 & 0x100010001000100ULL);
        r24 = ((r24 - r32) + (r32 >> 8));
        r32 = (((r25 << 16) & 0xff000000ff0000ULL)
            | ((r25 & 0xff000000ff0000ULL) >> 16));
        r25 = ((r25 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r25 & 0x100010001000100ULL);
        r25 = ((r25 - r32) + (r32 >> 8));
        r32 = (((r26 << 16) & 0xff000000ff0000ULL)
            | ((r26 & 0xff000000ff0000ULL) >> 16));
        r26 = ((r26 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r26 & 0x100010001000100ULL);
        r26 = ((r26 - r32) + (r32 >> 8));
        r32 = (((r27 << 16) & 0xff000000ff0000ULL)
            | ((r27 & 0xff000000ff0000ULL) >> 16));
        r27 = ((r27 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r27 & 0x100010001000100ULL);
        r27 = ((r27 - r32) + (r32 >> 8));
        r32 = (((r28 << 16) & 0xff000000ff0000ULL)
            | ((r28 & 0xff000000ff0000ULL) >> 16));
        r28 = ((r28 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r28 & 0x100010001000100ULL);
        r28 = ((r28 - r32) + (r32 >> 8));
        r32 = (((r29 << 16) & 0xff000000ff0000ULL)
            | ((r29 & 0xff000000ff0000ULL) >> 16));
        r29 = ((r29 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r29 & 0x100010001000100ULL);
        r29 = ((r29 - r32) + (r32 >> 8));
        r32 = (((r30 << 16) & 0xff000000ff0000ULL)
            | ((r30 & 0xff000000ff0000ULL) >> 16));
        r30 = ((r30 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r30 & 0x100010001000100ULL);
        r30 = ((r30 - r32) + (r32 >> 8));
        r32 = (((r31 << 16) & 0xff000000ff0000ULL)
            | ((r31 & 0xff000000ff0000ULL) >> 16));
        r31 = ((r31 ^ 0xff000000ff0000ULL) + r32);
        r32 = (r31 & 0x100010001000100ULL);
        r31 = ((r31 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r32 = (r0 + (r1 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r1);
        r1 = (r32 & 0x100010001000100ULL);
        r1 = ((r32 - r1) + (r1 >> 8));
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (r2 + (r3 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r3);
        r3 = (r32 & 0x100010001000100ULL);
        r3 = ((r32 - r3) + (r3 >> 8));
        r32 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r32) + (r32 >> 8));
        r32 = (r4 + (r5 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r5);
        r5 = (r32 & 0x100010001000100ULL);
        r5 = ((r32 - r5) + (r5 >> 8));
        r32 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r32) + (r32 >> 8));
        r32 = (r6 + (r7 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r7);
        r7 = (r32 & 0x100010001000100ULL);
        r7 = ((r32 - r7) + (r7 >> 8));
        r32 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r32) + (r32 >> 8));
        r32 = (r8 + (r9 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r9);
        r9 = (r32 & 0x100010001000100ULL);
        r9 = ((r32 - r9) + (r9 >> 8));
        r32 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r32) + (r32 >> 8));
        r32 = (r10 + (r11 ^ 0xff00ff00ff00ffULL));
        r10 = (r10 + r11);
        r11 = (r32 & 0x100010001000100ULL);
        r11 = ((r32 - r11) + (r11 >> 8));
        r32 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r32) + (r32 >> 8));
        r32 = (r12 + (r13 ^ 0xff00ff00ff00ffULL));
        r12 = (r12 + r13);
        r13 = (r32 & 0x100010001000100ULL);
        r13 = ((r32 - r13) + (r13 >> 8));
        r32 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r32) + (r32 >> 8));
        r32 = (r14 + (r15 ^ 0xff00ff00ff00ffULL));
        r14 = (r14 + r15);
        r15 = (r32 & 0x100010001000100ULL);
        r15 = ((r32 - r15) + (r15 >> 8));
        r32 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r32) + (r32 >> 8));
        r32 = (r16 + (r17 ^ 0xff00ff00ff00ffULL));
        r16 = (r16 + r17);
        r17 = (r32 & 0x100010001000100ULL);
        r17 = ((r32 - r17) + (r17 >> 8));
        r32 = (r16 & 0x100010001000100ULL);
        r16 = ((r16 - r32) + (r32 >> 8));
        r32 = (r18 + (r19 ^ 0xff00ff00ff00ffULL));
        r18 = (r18 + r19);
        r19 = (r32 & 0x100010001000100ULL);
        r19 = ((r32 - r19) + (r19 >> 8));
        r32 = (r18 & 0x100010001000100ULL);
        r18 = ((r18 - r32) + (r32 >> 8));
        r32 = (r20 + (r21 ^ 0xff00ff00ff00ffULL));
        r20 = (r20 + r21);
        r21 = (r32 & 0x100010001000100ULL);
        r21 = ((r32 - r21) + (r21 >> 8));
        r32 = (r20 & 0x100010001000100ULL);
        r20 = ((r20 - r32) + (r32 >> 8));
        r32 = (r22 + (r23 ^ 0xff00ff00ff00ffULL));
        r22 = (r22 + r23);
        r23 = (r32 & 0x100010001000100ULL);
        r23 = ((r32 - r23) + (r23 >> 8));
        r32 = (r22 & 0x100010001000100ULL);
        r22 = ((r22 - r32) + (r32 >> 8));
        r32 = (r24 + (r25 ^ 0xff00ff00ff00ffULL));
        r24 = (r24 + r25);
        r25 = (r32 & 0x100010001000100ULL);
        r25 = ((r32 - r25) + (r25 >> 8));
        r32 = (r24 & 0x100010001000100ULL);
        r24 = ((r24 - r32) + (r32 >> 8));
        r32 = (r26 + (r27 ^ 0xff00ff00ff00ffULL));
        r26 = (r26 + r27);
        r27 = (r32 & 0x100010001000100ULL);
        r27 = ((r32 - r27) + (r27 >> 8));
        r32 = (r26 & 0x100010001000100ULL);
        r26 = ((r26 - r32) + (r32 >> 8));
        r32 = (r28 + (r29 ^ 0xff00ff00ff00ffULL));
        r28 = (r28 + r29);
        r29 = (r32 & 0x100010001000100ULL);
        r29 = ((r32 - r29) + (r29 >> 8));
        r32 = (r28 & 0x100010001000100ULL);
        r28 = ((r28 - r32) + (r32 >> 8));
        r32 = (r30 + (r31 ^ 0xff00ff00ff00ffULL));
        r30 = (r30 + r31);
        r31 = (r32 & 0x100010001000100ULL);
        r31 = ((r32 - r31) + (r31 >> 8));
        r32 = (r30 & 0x100010001000100ULL);
        r30 = ((r30 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r32 = (r0 + (r2 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r2);
        r2 = (r32 & 0x100010001000100ULL);
        r2 = ((r32 - r2) + (r2 >> 8));
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (r1 + (r3 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r3);
        r3 = (r32 & 0x100010001000100ULL);
        r3 = ((r32 - r3) + (r3 >> 8));
        r32 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r32) + (r32 >> 8));
        r32 = (r4 + (r6 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r6);
        r6 = (r32 & 0x100010001000100ULL);
        r6 = ((r32 - r6) + (r6 >> 8));
        r32 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r32) + (r32 >> 8));
        r32 = (r5 + (r7 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r7);
        r7 = (r32 & 0x100010001000100ULL);
        r7 = ((r32 - r7) + (r7 >> 8));
        r32 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r32) + (r32 >> 8));
        r32 = (r8 + (r10 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r10);
        r10 = (r32 & 0x100010001000100ULL);
        r10 = ((r32 - r10) + (r10 >> 8));
        r32 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r32) + (r32 >> 8));
        r32 = (r9 + (r11 ^ 0xff00ff00ff00ffULL));
        r9 = (r9 + r11);
        r11 = (r32 & 0x100010001000100ULL);
        r11 = ((r32 - r11) + (r11 >> 8));
        r32 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r32) + (r32 >> 8));
        r32 = (r12 + (r14 ^ 0xff00ff00ff00ffULL));
        r12 = (r12 + r14);
        r14 = (r32 & 0x100010001000100ULL);
        r14 = ((r32 - r14) + (r14 >> 8));
        r32 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r32) + (r32 >> 8));
        r32 = (r13 + (r15 ^ 0xff00ff00ff00ffULL));
        r13 = (r13 + r15);
        r15 = (r32 & 0x100010001000100ULL);
        r15 = ((r32 - r15) + (r15 >> 8));
        r32 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r32) + (r32 >> 8));
        r32 = (r16 + (r18 ^ 0xff00ff00ff00ffULL));
        r16 = (r16 + r18);
        r18 = (r32 & 0x100010001000100ULL);
        r18 = ((r32 - r18) + (r18 >> 8));
        r32 = (r16 & 0x100010001000100ULL);
        r16 = ((r16 - r32) + (r32 >> 8));
        r32 = (r17 + (r19 ^ 0xff00ff00ff00ffULL));
        r17 = (r17 + r19);
        r19 = (r32 & 0x100010001000100ULL);
        r19 = ((r32 - r19) + (r19 >> 8));
        r32 = (r17 & 0x100010001000100ULL);
        r17 = ((r17 - r32) + (r32 >> 8));
        r32 = (r20 + (r22 ^ 0xff00ff00ff00ffULL));
        r20 = (r20 + r22);
        r22 = (r32 & 0x100010001000100ULL);
        r22 = ((r32 - r22) + (r22 >> 8));
        r32 = (r20 & 0x100010001000100ULL);
        r20 = ((r20 - r32) + (r32 >> 8));
        r32 = (r21 + (r23 ^ 0xff00ff00ff00ffULL));
        r21 = (r21 + r23);
        r23 = (r32 & 0x100010001000100ULL);
        r23 = ((r32 - r23) + (r23 >> 8));
        r32 = (r21 & 0x100010001000100ULL);
        r21 = ((r21 - r32) + (r32 >> 8));
        r32 = (r24 + (r26 ^ 0xff00ff00ff00ffULL));
        r24 = (r24 + r26);
        r26 = (r32 & 0x100010001000100ULL);
        r26 = ((r32 - r26) + (r26 >> 8));
        r32 = (r24 & 0x100010001000100ULL);
        r24 = ((r24 - r32) + (r32 >> 8));
        r32 = (r25 + (r27 ^ 0xff00ff00ff00ffULL));
        r25 = (r25 + r27);
        r27 = (r32 & 0x100010001000100ULL);
        r27 = ((r32 - r27) + (r27 >> 8));
        r32 = (r25 & 0x100010001000100ULL);
        r25 = ((r25 - r32) + (r32 >> 8));
        r32 = (r28 + (r30 ^ 0xff00ff00ff00ffULL));
        r28 = (r28 + r30);
        r30 = (r32 & 0x100010001000100ULL);
        r30 = ((r32 - r30) + (r30 >> 8));
        r32 = (r28 & 0x100010001000100ULL);
        r28 = ((r28 - r32) + (r32 >> 8));
        r32 = (r29 + (r31 ^ 0xff00ff00ff00ffULL));
        r29 = (r29 + r31);
        r31 = (r32 & 0x100010001000100ULL);
        r31 = ((r32 - r31) + (r31 >> 8));
        r32 = (r29 & 0x100010001000100ULL);
        r29 = ((r29 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r32 = (r0 + (r4 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r4);
        r4 = (r32 & 0x100010001000100ULL);
        r4 = ((r32 - r4) + (r4 >> 8));
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (r1 + (r5 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r5);
        r5 = (r32 & 0x100010001000100ULL);
        r5 = ((r32 - r5) + (r5 >> 8));
        r32 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r32) + (r32 >> 8));
        r32 = (r2 + (r6 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r6);
        r6 = (r32 & 0x100010001000100ULL);
        r6 = ((r32 - r6) + (r6 >> 8));
        r32 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r32) + (r32 >> 8));
        r32 = (r3 + (r7 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r7);
        r7 = (r32 & 0x100010001000100ULL);
        r7 = ((r32 - r7) + (r7 >> 8));
        r32 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r32) + (r32 >> 8));
        r32 = (r8 + (r12 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r12);
        r12 = (r32 & 0x100010001000100ULL);
        r12 = ((r32 - r12) + (r12 >> 8));
        r32 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r32) + (r32 >> 8));
        r32 = (r9 + (r13 ^ 0xff00ff00ff00ffULL));
        r9 = (r9 + r13);
        r13 = (r32 & 0x100010001000100ULL);
        r13 = ((r32 - r13) + (r13 >> 8));
        r32 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r32) + (r32 >> 8));
        r32 = (r10 + (r14 ^ 0xff00ff00ff00ffULL));
        r10 = (r10 + r14);
        r14 = (r32 & 0x100010001000100ULL);
        r14 = ((r32 - r14) + (r14 >> 8));
        r32 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r32) + (r32 >> 8));
        r32 = (r11 + (r15 ^ 0xff00ff00ff00ffULL));
        r11 = (r11 + r15);
        r15 = (r32 & 0x100010001000100ULL);
        r15 = ((r32 - r15) + (r15 >> 8));
        r32 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r32) + (r32 >> 8));
        r32 = (r16 + (r20 ^ 0xff00ff00ff00ffULL));
        r16 = (r16 + r20);
        r20 = (r32 & 0x100010001000100ULL);
        r20 = ((r32 - r20) + (r20 >> 8));
        r32 = (r16 & 0x100010001000100ULL);
        r16 = ((r16 - r32) + (r32 >> 8));
        r32 = (r17 + (r21 ^ 0xff00ff00ff00ffULL));
        r17 = (r17 + r21);
        r21 = (r32 & 0x100010001000100ULL);
        r21 = ((r32 - r21) + (r21 >> 8));
        r32 = (r17 & 0x100010001000100ULL);
        r17 = ((r17 - r32) + (r32 >> 8));
        r32 = (r18 + (r22 ^ 0xff00ff00ff00ffULL));
        r18 = (r18 + r22);
        r22 = (r32 & 0x100010001000100ULL);
        r22 = ((r32 - r22) + (r22 >> 8));
        r32 = (r18 & 0x100010001000100ULL);
        r18 = ((r18 - r32) + (r32 >> 8));
        r32 = (r19 + (r23 ^ 0xff00ff00ff00ffULL));
        r19 = (r19 + r23);
        r23 = (r32 & 0x100010001000100ULL);
        r23 = ((r32 - r23) + (r23 >> 8));
        r32 = (r19 & 0x100010001000100ULL);
        r19 = ((r19 - r32) + (r32 >> 8));
        r32 = (r24 + (r28 ^ 0xff00ff00ff00ffULL));
        r24 = (r24 + r28);
        r28 = (r32 & 0x100010001000100ULL);
        r28 = ((r32 - r28) + (r28 >> 8));
        r32 = (r24 & 0x100010001000100ULL);
        r24 = ((r24 - r32) + (r32 >> 8));
        r32 = (r25 + (r29 ^ 0xff00ff00ff00ffULL));
        r25 = (r25 + r29);
        r29 = (r32 & 0x100010001000100ULL);
        r29 = ((r32 - r29) + (r29 >> 8));
        r32 = (r25 & 0x100010001000100ULL);
        r25 = ((r25 - r32) + (r32 >> 8));
        r32 = (r26 + (r30 ^ 0xff00ff00ff00ffULL));
        r26 = (r26 + r30);
        r30 = (r32 & 0x100010001000100ULL);
        r30 = ((r32 - r30) + (r30 >> 8));
        r32 = (r26 & 0x100010001000100ULL);
        r26 = ((r26 - r32) + (r32 >> 8));
        r32 = (r27 + (r31 ^ 0xff00ff00ff00ffULL));
        r27 = (r27 + r31);
        r31 = (r32 & 0x100010001000100ULL);
        r31 = ((r32 - r31) + (r31 >> 8));
        r32 = (r27 & 0x100010001000100ULL);
        r27 = ((r27 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r32 = (r0 + (r8 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r8);
        r8 = (r32 & 0x100010001000100ULL);
        r8 = ((r32 - r8) + (r8 >> 8));
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (r1 + (r9 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r9);
        r9 = (r32 & 0x100010001000100ULL);
        r9 = ((r32 - r9) + (r9 >> 8));
        r32 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r32) + (r32 >> 8));
        r32 = (r2 + (r10 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r10);
        r10 = (r32 & 0x100010001000100ULL);
        r10 = ((r32 - r10) + (r10 >> 8));
        r32 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r32) + (r32 >> 8));
        r32 = (r3 + (r11 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r11);
        r11 = (r32 & 0x100010001000100ULL);
        r11 = ((r32 - r11) + (r11 >> 8));
        r32 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r32) + (r32 >> 8));
        r32 = (r4 + (r12 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r12);
        r12 = (r32 & 0x100010001000100ULL);
        r12 = ((r32 - r12) + (r12 >> 8));
        r32 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r32) + (r32 >> 8));
        r32 = (r5 + (r13 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r13);
        r13 = (r32 & 0x100010001000100ULL);
        r13 = ((r32 - r13) + (r13 >> 8));
        r32 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r32) + (r32 >> 8));
        r32 = (r6 + (r14 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r14);
        r14 = (r32 & 0x100010001000100ULL);
        r14 = ((r32 - r14) + (r14 >> 8));
        r32 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r32) + (r32 >> 8));
        r32 = (r7 + (r15 ^ 0xff00ff00ff00ffULL));
        r7 = (r7 + r15);
        r15 = (r32 & 0x100010001000100ULL);
        r15 = ((r32 - r15) + (r15 >> 8));
        r32 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r32) + (r32 >> 8));
        r32 = (r16 + (r24 ^ 0xff00ff00ff00ffULL));
        r16 = (r16 + r24);
        r24 = (r32 & 0x100010001000100ULL);
        r24 = ((r32 - r24) + (r24 >> 8));
        r32 = (r16 & 0x100010001000100ULL);
        r16 = ((r16 - r32) + (r32 >> 8));
        r32 = (r17 + (r25 ^ 0xff00ff00ff00ffULL));
        r17 = (r17 + r25);
        r25 = (r32 & 0x100010001000100ULL);
        r25 = ((r32 - r25) + (r25 >> 8));
        r32 = (r17 & 0x100010001000100ULL);
        r17 = ((r17 - r32) + (r32 >> 8));
        r32 = (r18 + (r26 ^ 0xff00ff00ff00ffULL));
        r18 = (r18 + r26);
        r26 = (r32 & 0x100010001000100ULL);
        r26 = ((r32 - r26) + (r26 >> 8));
        r32 = (r18 & 0x100010001000100ULL);
        r18 = ((r18 - r32) + (r32 >> 8));
        r32 = (r19 + (r27 ^ 0xff00ff00ff00ffULL));
        r19 = (r19 + r27);
        r27 = (r32 & 0x100010001000100ULL);
        r27 = ((r32 - r27) + (r27 >> 8));
        r32 = (r19 & 0x100010001000100ULL);
        r19 = ((r19 - r32) + (r32 >> 8));
        r32 = (r20 + (r28 ^ 0xff00ff00ff00ffULL));
        r20 = (r20 + r28);
        r28 = (r32 & 0x100010001000100ULL);
        r28 = ((r32 - r28) + (r28 >> 8));
        r32 = (r20 & 0x100010001000100ULL);
        r20 = ((r20 - r32) + (r32 >> 8));
        r32 = (r21 + (r29 ^ 0xff00ff00ff00ffULL));
        r21 = (r21 + r29);
        r29 = (r32 & 0x100010001000100ULL);
        r29 = ((r32 - r29) + (r29 >> 8));
        r32 = (r21 & 0x100010001000100ULL);
        r21 = ((r21 - r32) + (r32 >> 8));
        r32 = (r22 + (r30 ^ 0xff00ff00ff00ffULL));
        r22 = (r22 + r30);
        r30 = (r32 & 0x100010001000100ULL);
        r30 = ((r32 - r30) + (r30 >> 8));
        r32 = (r22 & 0x100010001000100ULL);
        r22 = ((r22 - r32) + (r32 >> 8));
        r32 = (r23 + (r31 ^ 0xff00ff00ff00ffULL));
        r23 = (r23 + r31);
        r31 = (r32 & 0x100010001000100ULL);
        r31 = ((r32 - r31) + (r31 >> 8));
        r32 = (r23 & 0x100010001000100ULL);
        r23 = ((r23 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Butterfly: v[i], v[i+128] = v[i]+v[i+128], v[i]-v[i+128]
        r32 = (r0 + (r16 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r16);
        r16 = (r32 & 0x100010001000100ULL);
        r16 = ((r32 - r16) + (r16 >> 8));
        r32 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r32) + (r32 >> 8));
        r32 = (r1 + (r17 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r17);
        r17 = (r32 & 0x100010001000100ULL);
        r17 = ((r32 - r17) + (r17 >> 8));
        r32 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r32) + (r32 >> 8));
        r32 = (r2 + (r18 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r18);
        r18 = (r32 & 0x100010001000100ULL);
        r18 = ((r32 - r18) + (r18 >> 8));
        r32 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r32) + (r32 >> 8));
        r32 = (r3 + (r19 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r19);
        r19 = (r32 & 0x100010001000100ULL);
        r19 = ((r32 - r19) + (r19 >> 8));
        r32 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r32) + (r32 >> 8));
        r32 = (r4 + (r20 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r20);
        r20 = (r32 & 0x100010001000100ULL);
        r20 = ((r32 - r20) + (r20 >> 8));
        r32 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r32) + (r32 >> 8));
        r32 = (r5 + (r21 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r21);
        r21 = (r32 & 0x100010001000100ULL);
        r21 = ((r32 - r21) + (r21 >> 8));
        r32 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r32) + (r32 >> 8));
        r32 = (r6 + (r22 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r22);
        r22 = (r32 & 0x100010001000100ULL);
        r22 = ((r32 - r22) + (r22 >> 8));
        r32 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r32) + (r32 >> 8));
        r32 = (r7 + (r23 ^ 0xff00ff00ff00ffULL));
        r7 = (r7 + r23);
        r23 = (r32 & 0x100010001000100ULL);
        r23 = ((r32 - r23) + (r23 >> 8));
        r32 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r32) + (r32 >> 8));
        r32 = (r8 + (r24 ^ 0xff00ff00ff00ffULL));
        r8 = (r8 + r24);
        r24 = (r32 & 0x100010001000100ULL);
        r24 = ((r32 - r24) + (r24 >> 8));
        r32 = (r8 & 0x100010001000100ULL);
        r8 = ((r8 - r32) + (r32 >> 8));
        r32 = (r9 + (r25 ^ 0xff00ff00ff00ffULL));
        r9 = (r9 + r25);
        r25 = (r32 & 0x100010001000100ULL);
        r25 = ((r32 - r25) + (r25 >> 8));
        r32 = (r9 & 0x100010001000100ULL);
        r9 = ((r9 - r32) + (r32 >> 8));
        r32 = (r10 + (r26 ^ 0xff00ff00ff00ffULL));
        r10 = (r10 + r26);
        r26 = (r32 & 0x100010001000100ULL);
        r26 = ((r32 - r26) + (r26 >> 8));
        r32 = (r10 & 0x100010001000100ULL);
        r10 = ((r10 - r32) + (r32 >> 8));
        r32 = (r11 + (r27 ^ 0xff00ff00ff00ffULL));
        r11 = (r11 + r27);
        r27 = (r32 & 0x100010001000100ULL);
        r27 = ((r32 - r27) + (r27 >> 8));
        r32 = (r11 & 0x100010001000100ULL);
        r11 = ((r11 - r32) + (r32 >> 8));
        r32 = (r12 + (r28 ^ 0xff00ff00ff00ffULL));
        r12 = (r12 + r28);
        r28 = (r32 & 0x100010001000100ULL);
        r28 = ((r32 - r28) + (r28 >> 8));
        r32 = (r12 & 0x100010001000100ULL);
        r12 = ((r12 - r32) + (r32 >> 8));
        r32 = (r13 + (r29 ^ 0xff00ff00ff00ffULL));
        r13 = (r13 + r29);
        r29 = (r32 & 0x100010001000100ULL);
        r29 = ((r32 - r29) + (r29 >> 8));
        r32 = (r13 & 0x100010001000100ULL);
        r13 = ((r13 - r32) + (r32 >> 8));
        r32 = (r14 + (r30 ^ 0xff00ff00ff00ffULL));
        r14 = (r14 + r30);
        r30 = (r32 & 0x100010001000100ULL);
        r30 = ((r32 - r30) + (r30 >> 8));
        r32 = (r14 & 0x100010001000100ULL);
        r14 = ((r14 - r32) + (r32 >> 8));
        r32 = (r15 + (r31 ^ 0xff00ff00ff00ffULL));
        r15 = (r15 + r31);
        r31 = (r32 & 0x100010001000100ULL);
        r31 = ((r32 - r31) + (r31 >> 8));
        r32 = (r15 & 0x100010001000100ULL);
        r15 = ((r15 - r32) + (r32 >> 8));
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
        // Reverse expansion for Hadamard operation
        r0 ^= (r16 << 8);
        r1 ^= (r17 << 8);
        r2 ^= (r18 << 8);
        r3 ^= (r19 << 8);
        r4 ^= (r20 << 8);
        r5 ^= (r21 << 8);
        r6 ^= (r22 << 8);
        r7 ^= (r23 << 8);
        r8 ^= (r24 << 8);
        r9 ^= (r25 << 8);
        r10 ^= (r26 << 8);
        r11 ^= (r27 << 8);
        r12 ^= (r28 << 8);
        r13 ^= (r29 << 8);
        r14 ^= (r30 << 8);
        r15 ^= (r31 << 8);
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        r0 = (((r0 & 0x707070707070707ULL) << 5)
            | ((r0 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[0] = r0 ^  p_mask[6];
        r1 = (((r1 & 0x707070707070707ULL) << 5)
            | ((r1 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[4] = r1 ^  p_mask[6];
        r2 = (((r2 & 0x707070707070707ULL) << 5)
            | ((r2 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[8] = r2 ^  p_mask[6];
        r3 = (((r3 & 0x707070707070707ULL) << 5)
            | ((r3 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[12] = r3 ^  p_mask[4];
        r4 = (((r4 & 0x707070707070707ULL) << 5)
            | ((r4 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[16] = r4 ^  p_mask[6];
        r5 = (((r5 & 0x707070707070707ULL) << 5)
            | ((r5 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[20] = r5 ^  p_mask[4];
        r6 = (((r6 & 0x707070707070707ULL) << 5)
            | ((r6 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[24] = r6 ^  p_mask[4];
        r7 = (((r7 & 0x707070707070707ULL) << 5)
            | ((r7 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[28] = r7 ^  p_mask[4];
        r8 = (((r8 & 0x707070707070707ULL) << 5)
            | ((r8 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[32] = r8 ^  p_mask[6];
        r9 = (((r9 & 0x707070707070707ULL) << 5)
            | ((r9 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[36] = r9 ^  p_mask[4];
        r10 = (((r10 & 0x707070707070707ULL) << 5)
            | ((r10 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[40] = r10 ^  p_mask[4];
        r11 = (((r11 & 0x707070707070707ULL) << 5)
            | ((r11 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[44] = r11 ^  p_mask[4];
        r12 = (((r12 & 0x707070707070707ULL) << 5)
            | ((r12 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[48] = r12 ^  p_mask[4];
        r13 = (((r13 & 0x707070707070707ULL) << 5)
            | ((r13 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[52] = r13 ^  p_mask[4];
        r14 = (((r14 & 0x707070707070707ULL) << 5)
            | ((r14 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[56] = r14 ^  p_mask[4];
        r15 = (((r15 & 0x707070707070707ULL) << 5)
            | ((r15 & 0xf8f8f8f8f8f8f8f8ULL) >> 3));
        v_out[60] = r15 ^  p_mask[6];
        v_in++;
        v_out++;
        }
        v_out[0] = 0;
        v_out[4] = 0;
        v_out[8] = 0;
        v_out[12] = 0;
        v_out[16] = 0;
        v_out[20] = 0;
        v_out[24] = 0;
        v_out[28] = 0;
        v_out[32] = 0;
        v_out[36] = 0;
        v_out[40] = 0;
        v_out[44] = 0;
        v_out[48] = 0;
        v_out[52] = 0;
        v_out[56] = 0;
        v_out[60] = 0;
        v_in += 61;
        v_out += 61;
        }
        // End of automatically generated matrix operation.
 
    }
}  


static void mm_op255_xi_a(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i;
    uint_mmv_t e_mask =  -((uint_mmv_t)exp1 & 0x1ULL);
    for (i = 0; i < 6; ++i) {
        // %%MUL_MATRIX_XI16 v_in, e_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8;

        uint_fast32_t i;
        // TODO: write comment!!!
        // 
        for (i = 0; i < 3; ++i) {
        e_mask = ~(e_mask);
        r0 = v_in[0] ^  (0xffffff00ffffff00ULL & e_mask);
        r4 = ((r0 ^ (r0 >> 8)) & 0xff000000ff00ULL);
        r0 ^= (r4 | (r4 << 8));
        r1 = v_in[8] ^  (0xff000000ffULL & e_mask);
        r4 = ((r1 ^ (r1 >> 8)) & 0xff000000ff00ULL);
        r1 ^= (r4 | (r4 << 8));
        r2 = v_in[4] ^  (0xff000000ffULL & e_mask);
        r4 = ((r2 ^ (r2 >> 8)) & 0xff000000ff00ULL);
        r2 ^= (r4 | (r4 << 8));
        r3 = v_in[12] ^  (0xff000000ffULL & e_mask);
        r4 = ((r3 ^ (r3 >> 8)) & 0xff000000ff00ULL);
        r3 ^= (r4 | (r4 << 8));
        // Expansion for Hadamard operation:
        // There is no space for a carry bit between bit fields. So 
        // we move bit field 2*i + 1  to bit field 2*i + 32.
        r4 = ((r0 >> 8) & 0xff00ff00ff00ffULL);
        r0 = (r0 & 0xff00ff00ff00ffULL);
        r5 = ((r1 >> 8) & 0xff00ff00ff00ffULL);
        r1 = (r1 & 0xff00ff00ff00ffULL);
        r6 = ((r2 >> 8) & 0xff00ff00ff00ffULL);
        r2 = (r2 & 0xff00ff00ff00ffULL);
        r7 = ((r3 >> 8) & 0xff00ff00ff00ffULL);
        r3 = (r3 & 0xff00ff00ff00ffULL);
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r8 = (((r0 << 16) & 0xff000000ff0000ULL)
            | ((r0 & 0xff000000ff0000ULL) >> 16));
        r0 = ((r0 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r8) + (r8 >> 8));
        r8 = (((r1 << 16) & 0xff000000ff0000ULL)
            | ((r1 & 0xff000000ff0000ULL) >> 16));
        r1 = ((r1 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r8) + (r8 >> 8));
        r8 = (((r2 << 16) & 0xff000000ff0000ULL)
            | ((r2 & 0xff000000ff0000ULL) >> 16));
        r2 = ((r2 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r8) + (r8 >> 8));
        r8 = (((r3 << 16) & 0xff000000ff0000ULL)
            | ((r3 & 0xff000000ff0000ULL) >> 16));
        r3 = ((r3 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r8) + (r8 >> 8));
        r8 = (((r4 << 16) & 0xff000000ff0000ULL)
            | ((r4 & 0xff000000ff0000ULL) >> 16));
        r4 = ((r4 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r8) + (r8 >> 8));
        r8 = (((r5 << 16) & 0xff000000ff0000ULL)
            | ((r5 & 0xff000000ff0000ULL) >> 16));
        r5 = ((r5 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r8) + (r8 >> 8));
        r8 = (((r6 << 16) & 0xff000000ff0000ULL)
            | ((r6 & 0xff000000ff0000ULL) >> 16));
        r6 = ((r6 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r8) + (r8 >> 8));
        r8 = (((r7 << 16) & 0xff000000ff0000ULL)
            | ((r7 & 0xff000000ff0000ULL) >> 16));
        r7 = ((r7 ^ 0xff000000ff0000ULL) + r8);
        r8 = (r7 & 0x100010001000100ULL);
        r7 = ((r7 - r8) + (r8 >> 8));
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r8 = (r0 + (r1 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r1);
        r1 = (r8 & 0x100010001000100ULL);
        r1 = ((r8 - r1) + (r1 >> 8));
        r8 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r8) + (r8 >> 8));
        r8 = (r2 + (r3 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r3);
        r3 = (r8 & 0x100010001000100ULL);
        r3 = ((r8 - r3) + (r3 >> 8));
        r8 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r8) + (r8 >> 8));
        r8 = (r4 + (r5 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r5);
        r5 = (r8 & 0x100010001000100ULL);
        r5 = ((r8 - r5) + (r5 >> 8));
        r8 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r8) + (r8 >> 8));
        r8 = (r6 + (r7 ^ 0xff00ff00ff00ffULL));
        r6 = (r6 + r7);
        r7 = (r8 & 0x100010001000100ULL);
        r7 = ((r8 - r7) + (r7 >> 8));
        r8 = (r6 & 0x100010001000100ULL);
        r6 = ((r6 - r8) + (r8 >> 8));
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r8 = (r0 + (r2 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r2);
        r2 = (r8 & 0x100010001000100ULL);
        r2 = ((r8 - r2) + (r2 >> 8));
        r8 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r8) + (r8 >> 8));
        r8 = (r1 + (r3 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r3);
        r3 = (r8 & 0x100010001000100ULL);
        r3 = ((r8 - r3) + (r3 >> 8));
        r8 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r8) + (r8 >> 8));
        r8 = (r4 + (r6 ^ 0xff00ff00ff00ffULL));
        r4 = (r4 + r6);
        r6 = (r8 & 0x100010001000100ULL);
        r6 = ((r8 - r6) + (r6 >> 8));
        r8 = (r4 & 0x100010001000100ULL);
        r4 = ((r4 - r8) + (r8 >> 8));
        r8 = (r5 + (r7 ^ 0xff00ff00ff00ffULL));
        r5 = (r5 + r7);
        r7 = (r8 & 0x100010001000100ULL);
        r7 = ((r8 - r7) + (r7 >> 8));
        r8 = (r5 & 0x100010001000100ULL);
        r5 = ((r5 - r8) + (r8 >> 8));
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r8 = (r0 + (r4 ^ 0xff00ff00ff00ffULL));
        r0 = (r0 + r4);
        r4 = (r8 & 0x100010001000100ULL);
        r4 = ((r8 - r4) + (r4 >> 8));
        r8 = (r0 & 0x100010001000100ULL);
        r0 = ((r0 - r8) + (r8 >> 8));
        r8 = (r1 + (r5 ^ 0xff00ff00ff00ffULL));
        r1 = (r1 + r5);
        r5 = (r8 & 0x100010001000100ULL);
        r5 = ((r8 - r5) + (r5 >> 8));
        r8 = (r1 & 0x100010001000100ULL);
        r1 = ((r1 - r8) + (r8 >> 8));
        r8 = (r2 + (r6 ^ 0xff00ff00ff00ffULL));
        r2 = (r2 + r6);
        r6 = (r8 & 0x100010001000100ULL);
        r6 = ((r8 - r6) + (r6 >> 8));
        r8 = (r2 & 0x100010001000100ULL);
        r2 = ((r2 - r8) + (r8 >> 8));
        r8 = (r3 + (r7 ^ 0xff00ff00ff00ffULL));
        r3 = (r3 + r7);
        r7 = (r8 & 0x100010001000100ULL);
        r7 = ((r8 - r7) + (r7 >> 8));
        r8 = (r3 & 0x100010001000100ULL);
        r3 = ((r3 - r8) + (r8 >> 8));
        // Vector is now  r(i) for i = 0,1,2,3,4,5,6,7
        // Reverse expansion for Hadamard operation
        r0 ^= (r4 << 8);
        r1 ^= (r5 << 8);
        r2 ^= (r6 << 8);
        r3 ^= (r7 << 8);
        // Vector is now  r(i) for i = 0,1,2,3
        e_mask = ~(e_mask);
        r0 = (((r0 & 0x303030303030303ULL) << 6)
            | ((r0 & 0xfcfcfcfcfcfcfcfcULL) >> 2));
        v_out[0] = r0 ^ (e_mask & 0xffffff00ffffff00ULL);
        r1 = (((r1 & 0x303030303030303ULL) << 6)
            | ((r1 & 0xfcfcfcfcfcfcfcfcULL) >> 2));
        v_out[4] = r1 ^ (e_mask & 0xff000000ffULL);
        r2 = (((r2 & 0x303030303030303ULL) << 6)
            | ((r2 & 0xfcfcfcfcfcfcfcfcULL) >> 2));
        v_out[8] = r2 ^ (e_mask & 0xff000000ffULL);
        r3 = (((r3 & 0x303030303030303ULL) << 6)
            | ((r3 & 0xfcfcfcfcfcfcfcfcULL) >> 2));
        v_out[12] = r3 ^ (e_mask & 0xff000000ffULL);
        // 138 lines of code, 302 operations
        v_in++;
        v_out++;
        }
        v_out[0] = 0;
        v_out[4] = 0;
        v_out[8] = 0;
        v_out[12] = 0;
        v_in += 13;
        v_out += 13;
        }
        // End of automatically generated matrix operation.
 
    }
}  


// %%EXPORT p
void mm_op255_xi(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i, exp1;
 
    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 30936; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 =  (uint_mmv_t)exp - 0x1ULL;

    // Do monomial part, i.e. tags B, C, T, X
    // Caution: this uses v_out[MM_OP255_OFS_Z:] as temporary storage
    mm_op255_xi_mon(v_in, exp1, v_out);

    // Do tag A
    mm_op255_xi_a(v_in, exp1, v_out); 

    // Do tags X, Y
    for (i = 0; i < 4; ++i) {
        uint_mmv_t *p_src = v_in + MM_OP255_OFS_Z + (i << HALF_YZ_SHIFT);
        mm_op255_xi_yz(p_src, exp1, v_out + TAB255_XI64_OFFSET[exp1][i]);
    }
    
}


