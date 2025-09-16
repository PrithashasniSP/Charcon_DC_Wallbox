/**
 * styles.h
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#include "../../lvgl/lvgl.h"

#ifndef _STYLES_H_
#define _STYLES_H_

/** Typedef **/
typedef struct
{
  int elem_x_pos;
  int elem_y_pos;
  int elem_width;
  int elem_height;
} element_attribs;


extern lv_style_t style_scr_backdrop;
extern lv_style_t style_text_plug;
extern lv_style_t style_text_time;
extern lv_style_t style_header_bar;
extern lv_style_t style_header_text;
extern lv_style_t style_dc_text;
extern lv_style_t style_dc_ready;
extern lv_style_t style_check_text;
extern lv_style_t style_check_good;
extern lv_style_t style_vehicle_text;
extern lv_style_t style_progress_text;
extern lv_style_t style_stop_button;
extern lv_style_t style_start_button;
extern lv_style_t style_failure_text;
extern lv_style_t style_confg_text;
extern lv_style_t style_icon_text;
extern lv_style_t style_stop_text;
extern lv_style_t style_yellow_text;
extern lv_style_t style_blue_text;
extern lv_style_t style_green_text;
extern lv_style_t style_white_text;
extern lv_style_t style_total_text;
extern lv_style_t style_terminate_text;
extern lv_style_t style_unplugged_text;
extern lv_style_t style_user_btn;
extern lv_style_t style_keyboard;
extern lv_style_t style_keyboard_btn;
extern lv_style_t style_textbox;
extern lv_style_t style_red_button;
extern lv_style_t style_blue_button;
extern lv_style_t style_red_text;
extern lv_style_t style_page_bg;
extern lv_style_t style_numbox;
extern lv_style_t style_num_key;
extern lv_style_t style_log_text;
extern lv_style_t style_ta_rect;

extern void init_style();
extern void init_style_backdrop();

#endif