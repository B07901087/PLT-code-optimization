#ifndef __INIT_DATA_HPP__
#define __INIT_DATA_HPP__

#include "system.hpp"

void data_init(FPDATA* inA, FPDATA* inB, FPDATA* gold) {
    inA[0] = -3.0;
    inA[1] = -1.0;
    inA[2] = 1.0;
    inA[3] = -2.0;
    inA[4] = -1.0;
    inA[5] = -2.0;
    inA[6] = 3.0;
    inA[7] = 3.0;
    inA[8] = -1.0;
    inA[9] = -1.0;
    inA[10] = 1.0;
    inA[11] = -3.0;
    inA[12] = 2.0;
    inA[13] = 2.0;
    inA[14] = 1.0;
    inA[15] = -1.0;
    inA[16] = 1.0;
    inA[17] = -1.0;
    inA[18] = -1.0;
    inA[19] = 3.0;
    inA[20] = -1.0;
    inA[21] = -2.0;
    inA[22] = 3.0;
    inA[23] = 1.0;
    inB[0] = -2.0;
    inB[1] = -1.0;
    inB[2] = -1.0;
    inB[3] = -1.0;
    gold[0] = 2.0;
    gold[1] = -6.0;
    gold[2] = -1.0;
    gold[3] = 8.0;
    gold[4] = -3.0;
    gold[5] = 7.0;
}

void change_dim(int32_t* rows, int32_t* loaded_cols, int32_t* cols){
    *rows = 6;
    *loaded_cols = 4;
    *cols = 1;
}
#endif
