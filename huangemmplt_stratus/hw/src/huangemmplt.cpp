// Copyright (c) 2011-2024 Columbia University, System Level Design Group
// SPDX-License-Identifier: Apache-2.0

#include "huangemmplt.hpp"
#include "huangemmplt_directives.hpp"

// Functions

#include "huangemmplt_functions.hpp"

// Processes

void huangemmplt::load_input()
{

    // Reset
    {
        HLS_PROTO("load-reset");

        this->reset_load_input();

        // explicit PLM ports reset if any

        // User-defined reset code

        wait();
    }

    // Config
    /* <<--params-->> */
    int32_t rows;
    int32_t cols;
    int32_t loaded_cols;
    {
        HLS_PROTO("load-config");

        cfg.wait_for_config(); // config process
        conf_info_t config = this->conf_info.read();

        // User-defined config code
        /* <<--local-params-->> */
        rows = config.rows;
        cols = config.cols;
        loaded_cols = config.loaded_cols;
    }
    // ESP_REPORT_INFO("CPP -- load -- config done");


    



    // Load
    {
        HLS_PROTO("load-dma");
        wait();




        // std::cerr << "starting\n" << DMA_WORD_PER_BEAT << "\n";
        // if (operating_mode == 1) {
        // load A matrix
        // cols
        int a_length = loaded_cols * rows;
        uint32_t load_A_offset = 0;
        // loaded_cols, then rows
        // make rows becomes continuous
        for (int rem = a_length; rem > 0; rem -= PLM_IN_WORD) {
            // I am using 4*4 matrix to test, so PLM_IN_WORD is 16
            uint32_t len = rem > PLM_IN_WORD ? PLM_IN_WORD : rem;
            dma_info_t dma_info(load_A_offset / DMA_WORD_PER_BEAT, len / DMA_WORD_PER_BEAT, DMA_SIZE);
            load_A_offset += len;
            this->dma_read_ctrl.put(dma_info);

            for (uint16_t i = 0; i < len; i += DMA_WORD_PER_BEAT) {
                HLS_BREAK_DEP(A_ping);

                sc_dt::sc_bv<DMA_WIDTH> dataBv;

                dataBv = this->dma_read_chnl.get();
                wait();

                // Write to PLM (all DMA_WORD_PER_BEAT words in one cycle)
                for (uint16_t k = 0; k < DMA_WORD_PER_BEAT; k++) {
                    HLS_UNROLL_SIMPLE;
                    A_ping[i + k] = dataBv.range((k+1) * DATA_WIDTH - 1, k * DATA_WIDTH).to_int64();
                }
            }
            // this->load_compute_handshake();
        }
        // ESP_REPORT_INFO("CPP -- load -- A done");
        // std::cerr << "end loading A\n";

        int b_length = loaded_cols * cols;
        // std::cerr << "b_length: " << b_length << "\n";
        int load_B_offset = round_up(a_length, DMA_WORD_PER_BEAT);
        // loaded_cols, then cols
        // make cols becomes continuous
        for (int rem = b_length; rem > 0; rem -= PLM_IN_WORD) {
            // I am using 4*4 matrix to test, so PLM_IN_WORD is 16
            uint32_t len = rem > PLM_IN_WORD ? PLM_IN_WORD : rem;
            dma_info_t dma_info(load_B_offset / DMA_WORD_PER_BEAT, len / DMA_WORD_PER_BEAT, DMA_SIZE);
            load_B_offset += len;
            this->dma_read_ctrl.put(dma_info);

            for (uint16_t i = 0; i < len; i += DMA_WORD_PER_BEAT) {
                HLS_BREAK_DEP(B_ping);

                sc_dt::sc_bv<DMA_WIDTH> dataBv;

                dataBv = this->dma_read_chnl.get();
                wait();

                // Write to PLM (all DMA_WORD_PER_BEAT words in one cycle)
                for (uint16_t k = 0; k < DMA_WORD_PER_BEAT; k++) {
                    // ESP_REPORT_INFO("getting B[%d]\n", i*DMA_WORD_PER_BEAT + k);
                    HLS_UNROLL_SIMPLE;
                    B_ping[i + k] = dataBv.range((k+1) * DATA_WIDTH - 1, k * DATA_WIDTH).to_int64();
                }
            }
            // this->load_compute_handshake();
        }
        // std::cerr << "end loading B\n";
        // ESP_REPORT_INFO("CPP -- load -- B done");

        // for (int i = 0; i < loaded_cols*rows; i++) {
        //     ESP_REPORT_INFO("A[%d] = %d", i, A_ping[i].to_int64());
        // }
        // for (int i = 0; i < loaded_cols*cols; i++) {
        //     ESP_REPORT_INFO("B[%d] = %d", i, B_ping[i].to_int64());
        // }

        // currently we don't consider ping pong, we just do handshake after the load operation
        
        this->load_compute_handshake();

        

        
        // ESP_REPORT_INFO("end load compute handshake");
    }



    // Conclude
    {
        this->process_done();
    }
}



void huangemmplt::store_output()
{
    // Reset
    {
        HLS_PROTO("store-reset");

        this->reset_store_output();

        // explicit PLM ports reset if any

        // User-defined reset code

        wait();
    }

    // Config
    /* <<--params-->> */
    int32_t rows;
    int32_t cols;
    int32_t loaded_cols;
    {
        HLS_PROTO("store-config");

        cfg.wait_for_config(); // config process
        conf_info_t config = this->conf_info.read();

        // User-defined config code
        /* <<--local-params-->> */
        rows = config.rows;
        cols = config.cols;
        loaded_cols = config.loaded_cols;
    }

    // Store
    {

        HLS_PROTO("store-dma");
        wait();
        bool ping = true;

        

        bool pingA = true;
        bool pingB = true;

        // uint32_t store_offset = round_up(loaded_cols*cols, DMA_WORD_PER_BEAT) * rows;
        // uint32_t offset = store_offset;

        // TPH: I don't really understand when the offset does not start from zero
        // The offset is sizeA + sizeB

     
        uint32_t store_O_offset = (round_up(loaded_cols*cols, DMA_WORD_PER_BEAT) + round_up(loaded_cols*rows, DMA_WORD_PER_BEAT));

        wait();

        uint32_t length = round_up(rows*cols, DMA_WORD_PER_BEAT);

        // store the result here
        // the dimension is 4*4 = 16, which is also PLM_OUT_WORD.
        
        
        for (int rem = length; rem > 0; rem -= PLM_OUT_WORD)
        {
            this->store_compute_handshake();
            // ESP_REPORT_INFO("end store compute handshake");
            uint32_t len = rem > PLM_OUT_WORD ? PLM_OUT_WORD : rem;
            dma_info_t dma_info(store_O_offset / DMA_WORD_PER_BEAT, len / DMA_WORD_PER_BEAT, DMA_SIZE);
            this->dma_write_ctrl.put(dma_info);
            
            
            
            for (uint16_t i = 0; i < len; i += DMA_WORD_PER_BEAT)
            {
                sc_dt::sc_bv<DMA_WIDTH> dataBv;

                // Read from PLM
                wait();
                for (uint16_t k = 0; k < DMA_WORD_PER_BEAT; k++)
                {
                    HLS_UNROLL_SIMPLE;
                    dataBv.range((k+1) * DATA_WIDTH - 1, k * DATA_WIDTH) = O_ping[i + k];
                        
                }
                // ESP_REPORT_INFO("before put");
                this->dma_write_chnl.put(dataBv);
                // ESP_REPORT_INFO("after put");
            }
        }

        

    }

    // for(int i = 0; i < 16; i++) {
    //     ESP_REPORT_INFO("O_ping[%d] = %d\n", i, O_ping[i].to_int64());
    // }
    // Conclude
    {
        this->accelerator_done();
        this->process_done();
    }
}


void huangemmplt::compute_kernel()
{
    // Reset
    {
        HLS_PROTO("compute-reset");

        this->reset_compute_kernel();

        // explicit PLM ports reset if any

        // User-defined reset code

        wait();
    }

    // Config
    /* <<--params-->> */
    int32_t rows;
    int32_t cols;
    int32_t loaded_cols;
    {
        HLS_PROTO("compute-config");

        cfg.wait_for_config(); // config process
        conf_info_t config = this->conf_info.read();

        // User-defined config code
        /* <<--local-params-->> */
        rows = config.rows;
        cols = config.cols;
        loaded_cols = config.loaded_cols;
    }


    // Compute
    {
        HLS_PROTO("compute-real");
        
        // ESP_REPORT_INFO("end compute load handshake");

        // we need to plan how much to load based on the current configuration
        // we need to block the case that (1 + cols) > plm size
        
        
        

        // the original output matrix is zero, and we are going to add sub_result again and again
        for(int i = 0; i < PLM_OUT_WORD; i++){
            O_ping[i] = 0;
            wait();
        }
        this -> compute_load_handshake();
        for (int i = 0; i < loaded_cols; i++){
            for (int j = 0; j < rows; j++) {
                for (int k = 0; k < cols; k++) {
                    // wait();
                    wait();
                    FPDATA tmp1 = int2fp<FPDATA, WORD_SIZE>(O_ping[j*cols + k]);
                    wait();
                    FPDATA tmp2 = int2fp<FPDATA, WORD_SIZE>(A_ping[i*rows + j]);
                    wait();
                    FPDATA tmp3 = int2fp<FPDATA, WORD_SIZE>(B_ping[i*cols + k]);
                    wait();
                    FPDATA tmp4 = tmp1 + tmp2 * tmp3;
                    wait();
                    O_ping[j*cols + k] = fp2int<FPDATA, WORD_SIZE>(tmp4);
                    wait();

                }
                wait();
            }
            wait();
        }
        this->compute_store_handshake();
        
            
        
        
        // ESP_REPORT_INFO("end compute store handshake");
    }

    // Conclude
    {
        this->process_done();
    }

    
}
