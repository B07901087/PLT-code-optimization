// Copyright (c) 2011-2024 Columbia University, System Level Design Group
// SPDX-License-Identifier: Apache-2.0
#include <linux/of_device.h>
#include <linux/mm.h>

#include <asm/io.h>

#include <esp_accelerator.h>
#include <esp.h>

#include "huangemmplt_stratus.h"

#define DRV_NAME	"huangemmplt_stratus"

/* <<--regs-->> */
// #define HUANGEMMPLT_HUANGEMMPLT_N_REG 0x48
// #define HUANGEMMPLT_HUANGEMMPLT_VEC_REG 0x44
// #define HUANGEMMPLT_HUANGEMMPLT_LEN_REG 0x40

#define HUANGEMMPLT_ROWS_REG 0x48
#define HUANGEMMPLT_COLS_REG 0x44
#define HUANGEMMPLT_LOADED_COLS_REG 0x40

struct huangemmplt_stratus_device {
	struct esp_device esp;
};

static struct esp_driver huangemmplt_driver;

static struct of_device_id huangemmplt_device_ids[] = {
	{
		.name = "SLD_HUANGEMMPLT_STRATUS",
	},
	{
		.name = "eb_08a",
	},
	{
		.compatible = "sld,huangemmplt_stratus",
	},
	{ },
};

static int huangemmplt_devs;

static inline struct huangemmplt_stratus_device *to_huangemmplt(struct esp_device *esp)
{
	return container_of(esp, struct huangemmplt_stratus_device, esp);
}

static void huangemmplt_prep_xfer(struct esp_device *esp, void *arg)
{
	struct huangemmplt_stratus_access *a = arg;

	/* <<--regs-config-->> */
	iowrite32be(a->rows, esp->iomem + HUANGEMMPLT_ROWS_REG);
	iowrite32be(a->cols, esp->iomem + HUANGEMMPLT_COLS_REG);
	iowrite32be(a->loaded_cols, esp->iomem + HUANGEMMPLT_LOADED_COLS_REG);
	iowrite32be(a->src_offset, esp->iomem + SRC_OFFSET_REG);
	iowrite32be(a->dst_offset, esp->iomem + DST_OFFSET_REG);

}

static bool huangemmplt_xfer_input_ok(struct esp_device *esp, void *arg)
{
	/* struct huangemmplt_stratus_device *huangemmplt = to_huangemmplt(esp); */
	/* struct huangemmplt_stratus_access *a = arg; */

	return true;
}

static int huangemmplt_probe(struct platform_device *pdev)
{
	struct huangemmplt_stratus_device *huangemmplt;
	struct esp_device *esp;
	int rc;

	huangemmplt = kzalloc(sizeof(*huangemmplt), GFP_KERNEL);
	if (huangemmplt == NULL)
		return -ENOMEM;
	esp = &huangemmplt->esp;
	esp->module = THIS_MODULE;
	esp->number = huangemmplt_devs;
	esp->driver = &huangemmplt_driver;
	rc = esp_device_register(esp, pdev);
	if (rc)
		goto err;

	huangemmplt_devs++;
	return 0;
 err:
	kfree(huangemmplt);
	return rc;
}

static int __exit huangemmplt_remove(struct platform_device *pdev)
{
	struct esp_device *esp = platform_get_drvdata(pdev);
	struct huangemmplt_stratus_device *huangemmplt = to_huangemmplt(esp);

	esp_device_unregister(esp);
	kfree(huangemmplt);
	return 0;
}

static struct esp_driver huangemmplt_driver = {
	.plat = {
		.probe		= huangemmplt_probe,
		.remove		= huangemmplt_remove,
		.driver		= {
			.name = DRV_NAME,
			.owner = THIS_MODULE,
			.of_match_table = huangemmplt_device_ids,
		},
	},
	.xfer_input_ok	= huangemmplt_xfer_input_ok,
	.prep_xfer	= huangemmplt_prep_xfer,
	.ioctl_cm	= HUANGEMMPLT_STRATUS_IOC_ACCESS,
	.arg_size	= sizeof(struct huangemmplt_stratus_access),
};

static int __init huangemmplt_init(void)
{
	return esp_driver_register(&huangemmplt_driver);
}

static void __exit huangemmplt_exit(void)
{
	esp_driver_unregister(&huangemmplt_driver);
}

module_init(huangemmplt_init)
module_exit(huangemmplt_exit)

MODULE_DEVICE_TABLE(of, huangemmplt_device_ids);

MODULE_AUTHOR("Emilio G. Cota <cota@braap.org>");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("huangemmplt_stratus driver");
