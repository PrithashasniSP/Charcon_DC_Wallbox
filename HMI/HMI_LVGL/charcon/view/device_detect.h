/**
 * device_detect.h
 *
 * Created on: 11-Sep-2023
 * Author: PSI2COB
 */

#ifndef _DEVICE_DETECT_H_
#define _DEVICE_DETECT_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"

extern int PlugStatus1;
extern int PlugStatus2;
extern int PlugStatus3;

extern int HealthIcon1;
extern int HealthIcon2;
extern int HealthIcon3;

extern int CloudConnection;

extern lv_obj_t *configure_label;
extern lv_obj_t *please_conf;
extern lv_obj_t *img_error;
extern lv_obj_t *failure_label;
extern lv_obj_t *service_label;
extern lv_obj_t *img_failure;

/* Project Includes */
extern void wallbax_failure_status();
extern void wallbox_not_configured();

#endif