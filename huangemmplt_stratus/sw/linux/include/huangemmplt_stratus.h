// Copyright (c) 2011-2024 Columbia University, System Level Design Group
// SPDX-License-Identifier: Apache-2.0
#ifndef _HUANGEMMPLT_STRATUS_H_
#define _HUANGEMMPLT_STRATUS_H_

#ifdef __KERNEL__
#include <linux/ioctl.h>
#include <linux/types.h>
#else
#include <sys/ioctl.h>
#include <stdint.h>
#ifndef __user
#define __user
#endif
#endif /* __KERNEL__ */

#include <esp.h>
#include <esp_accelerator.h>

struct huangemmplt_stratus_access {
	struct esp_access esp;
	/* <<--regs-->> */
	unsigned rows;
	unsigned cols;
	unsigned loaded_cols;
	unsigned src_offset;
	unsigned dst_offset;
};

#define HUANGEMMPLT_STRATUS_IOC_ACCESS	_IOW ('S', 0, struct huangemmplt_stratus_access)

#endif /* _HUANGEMMPLT_STRATUS_H_ */
