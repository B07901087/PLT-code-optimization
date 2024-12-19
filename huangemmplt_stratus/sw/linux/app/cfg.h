// Copyright (c) 2011-2024 Columbia University, System Level Design Group
// SPDX-License-Identifier: Apache-2.0
#ifndef __ESP_CFG_000_H__
#define __ESP_CFG_000_H__

#include "libesp.h"
#include "huangemmplt_stratus.h"

typedef int32_t token_t;

/* <<--params-def-->> */
// #define HUANGEMMPLT_N 1
// #define HUANGEMMPLT_VEC 100
// #define HUANGEMMPLT_LEN 64

#define HUANGEMMPLT_ROWS 4
#define HUANGEMMPLT_COLS 1000
#define HUANGEMMPLT_LOADED_COLS 4

/* <<--params-->> */
const int32_t rows = HUANGEMMPLT_ROWS;
const int32_t cols = HUANGEMMPLT_COLS;
const int32_t loaded_cols = HUANGEMMPLT_LOADED_COLS;

// #define NACC 2

struct huangemmplt_stratus_access huangemmplt_cfg_000[] = {
	{
		/* <<--descriptor-->> */
		.rows = HUANGEMMPLT_ROWS,
		.cols = HUANGEMMPLT_COLS,
		.loaded_cols = HUANGEMMPLT_LOADED_COLS,
		.src_offset = 0,
		.dst_offset = 0,
		.esp.coherence = ACC_COH_NONE,
		.esp.p2p_store = 0,
		.esp.p2p_nsrcs = 0,
		.esp.p2p_srcs = {"", "", "", ""},
	}
};



// usage: esp_run(cfg_000, 2);
esp_thread_info_t cfg_000[] = {
	{
		.run = true,
		.devname = "huangemmplt_stratus.0",
		.ioctl_req = HUANGEMMPLT_STRATUS_IOC_ACCESS,
		.esp_desc = &(huangemmplt_cfg_000[0].esp),
	}
};

#endif /* __ESP_CFG_000_H__ */
