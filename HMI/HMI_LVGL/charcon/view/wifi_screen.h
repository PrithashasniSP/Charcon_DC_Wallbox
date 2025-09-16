/**
 * wifi_screen.h
 *
 * Created on: 07-Dec-2023
 * Author: PSI2COB
 */

#ifndef _WIFI_SCREEN_H_
#define _WIFI_SCREEN_H_


#include "../../lvgl/lvgl.h"

extern lv_obj_t *back_icon;
extern lv_obj_t *wifi_text;
extern lv_obj_t *network_bg;
extern lv_obj_t *no_wifi_text;
extern lv_obj_t *no_wifi_icon;
extern lv_obj_t *wifi_ta;
extern lv_obj_t *wifi_pwd;
extern lv_obj_t *inc_text;
extern lv_obj_t *wifi_keyboard;
extern lv_obj_t *user_name;
extern lv_obj_t *wf_pwd;

LV_IMG_DECLARE(cancel_icon)
LV_IMG_DECLARE(no_wifi)

extern void scr_wifi_page();
static void wifi_ta_event(lv_event_t * e);
extern void save_wifi_credentials(const char *username, const char *password);

#endif