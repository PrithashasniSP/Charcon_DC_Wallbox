/**
 * styles.c
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#include <math.h>
#include "../../lvgl/lvgl.h"
#include "styles.h"
#include "colors.h"

lv_style_t style_scr_backdrop;
lv_style_t style_text_plug;
lv_style_t style_text_time;
lv_style_t style_header_bar;
lv_style_t style_header_text;
lv_style_t style_dc_text;
lv_style_t style_dc_ready;
lv_style_t style_check_text;
lv_style_t style_check_good;
lv_style_t style_vehicle_text;
lv_style_t style_progress_text;
lv_style_t style_stop_button;
lv_style_t style_start_button;
lv_style_t style_failure_text;
lv_style_t style_confg_text;
lv_style_t style_icon_text;
lv_style_t style_stop_text;
lv_style_t style_yellow_text;
lv_style_t style_blue_text;
lv_style_t style_total_text;
lv_style_t style_terminate_text;
lv_style_t style_green_text;
lv_style_t style_white_text;
lv_style_t style_unplugged_text;
lv_style_t style_user_btn;
lv_style_t style_keyboard;
lv_style_t style_keyboard_btn;
lv_style_t style_textbox;
lv_style_t style_red_button;
lv_style_t style_blue_button;
lv_style_t style_red_text;
lv_style_t style_page_bg;
lv_style_t style_numbox;
lv_style_t style_num_key;
lv_style_t style_log_text; 
lv_style_t style_ta_rect; 

void init_style()
{
    init_style_backdrop();
}

void init_style_backdrop()
{
    lv_style_init(&style_scr_backdrop);
     lv_style_set_radius(&style_scr_backdrop, 0);
    lv_style_set_bg_color(&style_scr_backdrop, lv_color_hex(0x000000));
    lv_style_set_border_color(&style_scr_backdrop, lv_color_hex(0x000000));

    lv_style_init(&style_text_plug);
    // lv_style_set_text_color(&style_text_plug, lv_color_hex(0xFFFFFF));
    lv_style_set_text_font(&style_text_plug, &lv_font_montserrat_32);

    lv_style_init(&style_text_time);
    lv_style_set_text_color(&style_text_time, lv_color_hex(0xFFFFFF));
    lv_style_set_text_font(&style_text_time, &lv_font_montserrat_22);

    lv_style_init(&style_header_bar);
    lv_style_set_bg_color(&style_header_bar, lv_color_hex(0x848484));
    lv_style_set_border_color(&style_header_bar, lv_color_hex(0x848484));

    lv_style_init(&style_header_text);
    lv_style_set_text_color(&style_header_text, lv_color_hex(0x5c5c5c));
    lv_style_set_text_font(&style_header_text, &lv_font_montserrat_22);
    lv_style_set_text_letter_space(&style_header_text, 2);

    lv_style_init(&style_dc_text);
    lv_style_set_text_color(&style_dc_text, lv_color_hex(0xffdc64));
    lv_style_set_text_font(&style_dc_text, &lv_font_montserrat_42);

    lv_style_init(&style_dc_ready);
    lv_style_set_text_color(&style_dc_ready, LV_COLOR_GREEN);
    lv_style_set_text_font(&style_dc_ready, &lv_font_montserrat_40);

    lv_style_init(&style_check_text);
    lv_style_set_text_color(&style_check_text, lv_color_hex(0xFFFFFF));
    lv_style_set_text_font(&style_check_text, &lv_font_montserrat_28);

    lv_style_init(&style_check_good);
    lv_style_set_text_color(&style_check_good, LV_COLOR_GREEN);
    lv_style_set_text_font(&style_check_good, &lv_font_montserrat_28);

    lv_style_init(&style_vehicle_text);
    lv_style_set_text_color(&style_vehicle_text, LV_COLOR_BLUE);
    lv_style_set_text_font(&style_vehicle_text, &lv_font_montserrat_32);

    lv_style_init(&style_stop_button);
    lv_style_set_bg_color(&style_stop_button, LV_COLOR_RED);
    lv_style_set_clip_corner(&style_stop_button, true);
    lv_style_set_border_opa(&style_stop_button, LV_OPA_0);
    lv_style_set_radius(&style_stop_button, LV_RADIUS_CIRCLE);
    lv_style_set_shadow_width(&style_stop_button, 0);

    lv_style_init(&style_stop_text);
    lv_style_set_text_color(&style_stop_text, lv_color_hex(0xFFFFFF));
    lv_style_set_text_font(&style_stop_text, &lv_font_montserrat_34);

    lv_style_init(&style_start_button);
    lv_style_set_bg_color(&style_start_button, LV_COLOR_YELLOW);
    lv_style_set_clip_corner(&style_start_button, true);
    lv_style_set_border_opa(&style_start_button, LV_OPA_0);
    lv_style_set_radius(&style_start_button, LV_RADIUS_CIRCLE);
    lv_style_set_shadow_width(&style_start_button, 0);

    lv_style_init(&style_progress_text);
    lv_style_set_text_color(&style_progress_text, lv_color_hex(0x74ac44));
    lv_style_set_text_font(&style_progress_text, &lv_font_montserrat_38);
 
    lv_style_init(&style_failure_text);
    lv_style_set_text_color(&style_failure_text, lv_color_hex(0xff0404));
    lv_style_set_text_font(&style_failure_text, &lv_font_montserrat_36);

    lv_style_init(&style_confg_text);
    lv_style_set_text_color(&style_confg_text, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_confg_text, &lv_font_montserrat_36);

    lv_style_init(&style_icon_text);
    lv_style_set_text_color(&style_icon_text, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_icon_text, &lv_font_montserrat_12);

    lv_style_init(&style_yellow_text);
    lv_style_set_text_color(&style_yellow_text, lv_color_hex(0xf9c459));
    lv_style_set_text_font(&style_yellow_text, &lv_font_montserrat_26);

    lv_style_init(&style_blue_text);
    lv_style_set_text_color(&style_blue_text, lv_color_hex(0x44b6ce));
    lv_style_set_text_font(&style_blue_text, &lv_font_montserrat_26);

    lv_style_init(&style_total_text);
    lv_style_set_text_color(&style_total_text, lv_color_hex(0xf8b484));
    lv_style_set_text_font(&style_total_text, &lv_font_montserrat_38);

    lv_style_init(&style_terminate_text);
    lv_style_set_text_color(&style_terminate_text, LV_COLOR_RED);
    lv_style_set_text_font(&style_terminate_text, &lv_font_montserrat_38);

    lv_style_init(&style_green_text);
    lv_style_set_text_color(&style_green_text, LV_COLOR_GREEN);
    lv_style_set_text_font(&style_green_text, &lv_font_montserrat_40);

    lv_style_init(&style_white_text);
    lv_style_set_text_color(&style_white_text, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_white_text, &lv_font_montserrat_32);

    lv_style_init(&style_red_text);
    lv_style_set_text_color(&style_red_text, LV_COLOR_RED);
    lv_style_set_text_font(&style_red_text, &lv_font_montserrat_26);

    lv_style_init(&style_unplugged_text);
    lv_style_set_text_color(&style_unplugged_text, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_unplugged_text, &lv_font_montserrat_40);

    lv_style_init(&style_keyboard);
    lv_style_set_bg_opa(&style_keyboard, LV_OPA_0);
    lv_style_set_border_opa(&style_keyboard, LV_OPA_0);

    lv_style_init(&style_keyboard_btn);
    lv_style_set_bg_color(&style_keyboard_btn, lv_color_hex(0x6c6c6c));
    lv_style_set_border_color(&style_keyboard_btn, lv_color_hex(0x848484));
    lv_style_set_text_color(&style_keyboard_btn, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_keyboard_btn, &lv_font_montserrat_24);
    lv_style_set_width(&style_keyboard_btn, 5);
    lv_style_set_height(&style_keyboard_btn, 5);

    lv_style_init(&style_textbox);
    lv_style_set_text_color(&style_textbox, LV_COLOR_BLACK);
    lv_style_set_text_font(&style_textbox, &lv_font_montserrat_22);  
    lv_style_set_radius(&style_textbox, 0);

    lv_style_init(&style_log_text);
    lv_style_set_text_color(&style_log_text, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_log_text, &lv_font_montserrat_16);  
    lv_style_set_radius(&style_log_text, 0);

    lv_style_init(&style_numbox);
    lv_style_set_text_color(&style_numbox, LV_COLOR_BLACK);
    lv_style_set_text_font(&style_numbox, &lv_font_montserrat_32);  
    lv_style_set_radius(&style_numbox, 0);

    lv_style_init(&style_num_key);
    lv_style_set_bg_color(&style_num_key, lv_color_hex(0x6c6c6c));
    lv_style_set_border_color(&style_num_key, lv_color_hex(0x848484));
    lv_style_set_text_color(&style_num_key, LV_COLOR_WHITE);
    lv_style_set_text_font(&style_num_key, &lv_font_montserrat_28);
    lv_style_set_width(&style_num_key, 5);
    lv_style_set_height(&style_num_key, 5);

    lv_style_init(&style_red_button);
    lv_style_set_bg_color(&style_red_button, lv_color_hex(0xf00404));
    lv_style_set_clip_corner(&style_red_button, true);
    lv_style_set_border_color(&style_red_button, lv_color_hex(0xc40404));
    lv_style_set_radius(&style_red_button, 10);
    lv_style_set_border_width(&style_red_button, 3);
    lv_style_set_shadow_width(&style_red_button, 0);

    lv_style_init(&style_blue_button);
    lv_style_set_bg_color(&style_blue_button, lv_color_hex(0x4472c4));
    lv_style_set_clip_corner(&style_blue_button, true);
    lv_style_set_border_color(&style_blue_button, lv_color_hex(0x30508f));
    lv_style_set_radius(&style_blue_button, 10);
    lv_style_set_border_width(&style_blue_button, 3);
    lv_style_set_shadow_width(&style_blue_button, 0);

    lv_style_init(&style_page_bg);
    lv_style_set_bg_opa(&style_page_bg, LV_OPA_0);
    lv_style_set_border_color(&style_page_bg, LV_COLOR_WHITE);
    lv_style_set_border_width(&style_page_bg, 2);
    lv_style_set_radius(&style_page_bg, 0);

    lv_style_init(&style_ta_rect);
    lv_style_set_bg_opa(&style_ta_rect, LV_OPA_60);
    lv_style_set_bg_color(&style_ta_rect, LV_COLOR_GREY);
    lv_style_set_border_color(&style_ta_rect, LV_COLOR_LIGHT_GREY);
    lv_style_set_radius(&style_ta_rect, 0);
}

