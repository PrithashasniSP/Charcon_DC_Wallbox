/**
 * launch_screen.h
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */


#ifndef _LAUNCH_SCREEN_H_
#define _LAUNCH_SCREEN_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"

extern lv_obj_t *scr_home;
extern lv_obj_t *img_bosch_logo;
extern lv_obj_t *default_heading;

LV_IMG_DECLARE(bosch_logo)

/* Project Includes */
extern void create_launch_screen();
extern void img_animation(lv_obj_t *img_bosch_logo);
extern void display_allpage_icons();
extern void home_screen();

#endif