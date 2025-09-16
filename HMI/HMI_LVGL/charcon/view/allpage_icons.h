/**
 * allpage_icons.h
 *
 * Created on: 11-Sep-2023
 * Author: PSI2COB
 */

#ifndef _ALLPAGE_ICONS_H_
#define _ALLPAGE_ICONS_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"


extern lv_obj_t *img_profile;
extern lv_obj_t *img_wifi;
extern lv_obj_t *img_network;
extern lv_obj_t *img_location;
extern lv_obj_t *header_rect;
extern lv_obj_t *back_rect;
extern lv_obj_t *header_text;
extern lv_obj_t *label_location;
extern lv_obj_t *label_guest;
extern lv_obj_t *label_time;
extern lv_obj_t *img_footer;
extern lv_obj_t *bg_object;
extern lv_obj_t *img_charger;
extern lv_obj_t *bosch_footer;
extern lv_obj_t *label_plug;
extern lv_obj_t *img_plug;
extern lv_obj_t *img_health;
extern lv_obj_t *img_settings;
extern lv_obj_t *img_cloud;
extern lv_obj_t *img_home;
extern lv_obj_t *img_log;
extern lv_obj_t *img_vsecc;
extern lv_obj_t *img_charcon;
extern lv_obj_t *img_signal1;
extern lv_obj_t *img_signal2;
extern lv_obj_t *img_signal3;
extern lv_obj_t *img_signal4;
extern lv_obj_t *img_signal5;
extern lv_obj_t *img_wifi5;
extern lv_obj_t *img_wifi4;
extern lv_obj_t *img_wifi3;
extern lv_obj_t *img_wifi2;
extern lv_obj_t *img_wifi1;
extern lv_obj_t *img_no_wifi;
extern lv_obj_t *img_mc;
extern lv_obj_t *sw_text;
extern lv_obj_t *home_text;
extern lv_obj_t *log_text;
extern lv_obj_t *vsecc_text;
extern lv_obj_t *charcon_text;
extern lv_obj_t *mc_text;
extern lv_obj_t *img_cloud_connection;
extern lv_obj_t *img_arrow;
extern lv_obj_t *img_no_signal;

LV_IMG_DECLARE(charger)
LV_IMG_DECLARE(footer_logo)
LV_IMG_DECLARE(icon_not_plug)
LV_IMG_DECLARE(icon_connect)
LV_IMG_DECLARE(icon_charging)
LV_IMG_DECLARE(icon_profile)
LV_IMG_DECLARE(icon_wifi)
LV_IMG_DECLARE(icon_network)
LV_IMG_DECLARE(icon_location)
LV_IMG_DECLARE(icon_good)
LV_IMG_DECLARE(red_failure)
LV_IMG_DECLARE(white_confg)
LV_IMG_DECLARE(settings_icon)
LV_IMG_DECLARE(cloud_icon)
LV_IMG_DECLARE(home_icon)
LV_IMG_DECLARE(log_icon)
LV_IMG_DECLARE(vsecc_icon)
LV_IMG_DECLARE(charcon_icon)
LV_IMG_DECLARE(icon_connect_error)
LV_IMG_DECLARE(cloud_failure)
LV_IMG_DECLARE(cloud_connect)
LV_IMG_DECLARE(arrow_up)
LV_IMG_DECLARE(img_signal)
LV_IMG_DECLARE(img_network_1)
LV_IMG_DECLARE(img_network_2)
LV_IMG_DECLARE(img_network_3)
LV_IMG_DECLARE(img_network_4)
LV_IMG_DECLARE(img_network_5)
LV_IMG_DECLARE(wifi_5)
LV_IMG_DECLARE(wifi_4)
LV_IMG_DECLARE(wifi_3)
LV_IMG_DECLARE(wifi_2)
LV_IMG_DECLARE(wifi_1)
LV_IMG_DECLARE(img_no_network)

extern char g_position[1000];
extern double g_latitude;
extern double g_longitude;
extern int g_GSMsignal;
extern int Wifisignal;
extern int header_flag;
extern int char_count;
extern char admin_text[50];
extern const char *loc_text;
extern const char *start;
extern const int CONST_AdminLoginPage;
extern const int CONST_SoftwareUpdate;
extern const int CONST_VseccSettings;
extern const int CONST_CharconSettings;
extern const int CONST_MasterControl;
extern const int CONST_AdminLogsPage;
extern const int CONST_WiFiPage;


/* Project Includes */
extern void allpage_status();
extern void header_icons_display();
extern void scr_login();
extern void header_icons_close();
extern void header_icons_flag();
extern void header_loc_scroll();
extern void scr_sw_update();
extern void scr_vsecc_set();
extern void scr_charcon_set();
extern void scr_mc_set();
extern void scr_log_set();
extern void scr_wifi_set();
extern void health_check_status();
extern void get_current_datetime(char *datetime_str);
extern void scroll_location();
#endif