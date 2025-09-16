/**
 * health_check.h
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#ifndef _HEALTH_CHECK_H_
#define _HEALTH_CHECK_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"

extern lv_obj_t *img_red_check;
extern lv_obj_t *img_green_check;
extern lv_obj_t *label_dc_text;
extern lv_obj_t *cable_text;
extern lv_obj_t *power_text;
extern lv_obj_t *check1_text;
extern lv_obj_t *check2_text;
extern lv_obj_t *ready_text;
extern lv_obj_t *green_heart;
extern lv_obj_t *img_plug_connect;
extern lv_obj_t *connection_text;
extern lv_obj_t *vehicle_text;
extern lv_obj_t *start_button;
extern lv_obj_t *start_charging;
extern lv_obj_t *start_text;
extern lv_obj_t *img_initializing;
extern lv_obj_t *initialize_text;
extern lv_obj_t *scr_check;
extern lv_obj_t *check1_good;
extern lv_obj_t *check2_good;
extern lv_obj_t *scr_init;
extern lv_obj_t *test_b1;
extern lv_obj_t *test_b2;
extern lv_obj_t *scr_default;
extern lv_timer_t *check_task;

extern int PlugStatus;
extern int HealthIcon;
extern int CloudConnection;

extern int CableCheckStatus;
extern int PowerBoardStatus;
extern int HeartBeatMsg;

LV_IMG_DECLARE(green_check)
LV_IMG_DECLARE(red_check)
LV_IMG_DECLARE(img_loader)

/* Project Includes */
extern void screen_bosch_charger();
extern void screen_dc_check();
extern void cable_check_status();
extern void power_board_status();
extern void heart_beat_msg();
static void scr_health_check(lv_event_t *event);
extern void anim_opacity_cb(void *var, int32_t v);
extern void anim_rotate_cb(void * var, int32_t v);
extern void anim_zoom_cb(void *var, int32_t v);

extern void initialize_device();

void dc_animation_finished_callback(lv_anim_t *anim);
void dc2_animation_finished_callback(lv_anim_t *anim);
static void dc_check_complete(lv_event_t *event);
static void connection_screen(lv_event_t *event);
static void charge_start_stop(lv_event_t *event);
static void scr_charging(lv_event_t *event);
#endif