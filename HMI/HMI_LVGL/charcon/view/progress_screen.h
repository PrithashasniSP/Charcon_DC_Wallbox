/**
 * progress_screen.h
 *
 * Created on: 01-Sep-2023
 * Author: PSI2COB
 */

#ifndef _PROGRESS_SCREEN_H_
#define _PROGRESS_SCREEN_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"

extern lv_obj_t *img_money;
extern lv_obj_t *img_power;
extern lv_obj_t *chart1;
extern lv_obj_t *text_costgrid;
extern lv_obj_t *text_energy;
extern lv_obj_t *text_total;
extern lv_obj_t *stop_button;
extern lv_obj_t *stop_charging;
extern lv_obj_t *stop_text;
extern lv_obj_t *text_solar;
extern lv_obj_t *text_grid;
extern lv_obj_t *text_time_charging;
extern lv_obj_t *cost_text;
extern lv_obj_t *solar_energy_text;
extern lv_obj_t *grid_energy_text;
extern lv_obj_t *total_cost_value;
extern lv_obj_t *terminate_text;
extern lv_obj_t *charging_complete;
extern lv_obj_t *unplug_text;
extern lv_obj_t *timer_label;
extern lv_obj_t *img_terminate;
extern lv_obj_t *img_cost_unit;
extern lv_obj_t *img_tot_cost;
extern lv_obj_t *scr_progress;

extern lv_timer_t *timer_task;
extern lv_timer_t *progress_task;
extern lv_chart_series_t * ser1;
extern lv_chart_series_t * ser2;

extern int sec, min, hr;

LV_IMG_DECLARE(icon_money)
LV_IMG_DECLARE(icon_power)
LV_IMG_DECLARE(img_cost)
LV_IMG_DECLARE(img_tot)

extern int PlugStatus1;
extern int PlugStatus2;
extern int PlugStatus3;

extern int HealthIcon1;
extern int HealthIcon2;
extern int HealthIcon3;

extern char cost_on_grid[10];

/*Project Includes*/
extern void create_progress_screen();
extern void create_progress_chart();
extern void charge_timer_start();
static void draw_event_cb(lv_event_t *e);
extern void pub_stop(lv_event_t *event);
static void add_data(lv_timer_t * timer);
static int32_t round_fixed_point(int32_t n, int8_t shift);
static void slider_x_event_cb(lv_event_t * e);
extern void charging_progress_state();
void updateCircularBuffer(int newValue);

#endif