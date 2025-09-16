/**
 * admin_access.h
 *
 * Created on: 03-Oct-2023
 * Author: PSI2COB
 */

#ifndef _ADMIN_ACCESS_H_
#define _ADMIN_ACCESS_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"


extern lv_obj_t *scr_cloud;
extern lv_obj_t *scr_vsecc;
extern lv_obj_t *scr_charcon;
extern lv_obj_t *scr_master;
extern lv_obj_t *scr_logs;
extern lv_obj_t *img_log;
extern lv_obj_t *log_text;
extern lv_obj_t *logs_page;

extern lv_obj_t *updates_text;
extern lv_obj_t *img_init;
extern lv_obj_t *img_back;
extern lv_obj_t *back_text;
extern lv_obj_t *icon_vsecc;
extern lv_obj_t *vsecc_settings;
extern lv_obj_t *vehicle_label;
extern lv_obj_t *underline;
extern lv_obj_t *vehicle_num;
extern lv_obj_t *state_label;
extern lv_obj_t *state_value;
extern lv_obj_t *mode_label;
extern lv_obj_t *mode_value;
extern lv_obj_t *cancel_vsecc;
extern lv_obj_t *cancel_charcon;
extern lv_obj_t *icon_charcon;
extern lv_obj_t *charcon_settings;
extern lv_obj_t *charcon_current_limit;
extern lv_obj_t *charcon_mode_label;
extern lv_obj_t *charcon_current_label;
extern lv_obj_t *charcon_mode_value;
extern lv_obj_t *charcon_current_value;
extern lv_obj_t *voltage_label;
extern lv_obj_t *voltage_value;
extern lv_obj_t *charcon_ta;
extern lv_obj_t *charcon_keyboard_area;
extern lv_obj_t *rect_ta;
extern lv_obj_t *icon_mc;
extern lv_obj_t *mc_settings;
extern lv_obj_t *mc_current_limit;
extern lv_obj_t *mc_mode_label;
extern lv_obj_t *mc_mode_value;
extern lv_obj_t *mc_keyboard_area;
extern lv_obj_t *mc_ta;
extern lv_obj_t *rect_ta1;
extern lv_obj_t *cancel_mc;
extern lv_obj_t *icon_log;
extern lv_obj_t *logs_text;
extern lv_obj_t *logs_page;
extern lv_obj_t *cancel_logs;
extern lv_obj_t *vsecc_underline;
extern lv_obj_t *charcon_underline;
extern lv_obj_t *mc_underline;
extern lv_obj_t *logs_underline;
extern lv_obj_t *export_logs;
extern lv_obj_t *export_text;
extern lv_timer_t *rect_timer;
extern lv_timer_t *rect1_timer;
extern lv_timer_t *log_timer;

LV_IMG_DECLARE(back_button)

extern void scr_software_update();
extern void scr_vsecc_settings();
extern void scr_charcon_settings();
extern void scr_master_control();
extern void scr_logs_page();
static void ta_handler(lv_event_t * e);
static void btnm_event_handler(lv_event_t * e);
static void ta_vol_handler(lv_event_t * e);
static void btnm_event1_handler(lv_event_t * e);
extern void add_log();
extern void print_next_line();
extern void ta_rect_cb();
extern void ta1_rect_cb();

#endif