/**
 * launch_screen.c
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#include "../../lvgl/lvgl.h"
#include "launch_screen.h"
#include "health_check.h"
#include "styles.h"
#include "device_detect.h"
#include "allpage_icons.h"
#include "admin_page.h"
#include "../controller/controller.h"
#include "../../sub.h"
lv_obj_t *scr_home;
lv_obj_t *img_bosch_logo;
lv_obj_t *default_heading;

void create_launch_screen()
{
  scr_home = lv_obj_create(lv_scr_act());
  lv_obj_set_size(scr_home, 1280.5, 800.5);
  lv_obj_add_flag(scr_home,  LV_OBJ_FLAG_FLOATING);
  lv_obj_clear_flag(scr_home,  LV_OBJ_FLAG_CLICKABLE);
  lv_obj_set_scrollbar_mode(scr_home, LV_SCROLLBAR_MODE_OFF);
  lv_obj_add_style(scr_home, &style_scr_backdrop, LV_STATE_DEFAULT);

  img_bosch_logo = lv_img_create(scr_home);
  lv_img_set_src(img_bosch_logo, &bosch_logo);
  lv_obj_align(img_bosch_logo, LV_ALIGN_CENTER, 0, 0);

  allpage_status();
  lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);
  lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);
  create_progress_screen();

  img_animation(img_bosch_logo);
}

void img_animation(lv_obj_t *img_bosch_logo)
{
  lv_anim_t img;
  lv_anim_init(&img);
  lv_anim_set_exec_cb(&img, (lv_anim_exec_xcb_t)lv_img_set_zoom);
  lv_anim_set_var(&img, img_bosch_logo);
  lv_anim_set_time(&img, 250);
  lv_anim_set_delay(&img, 100);
  lv_anim_set_values(&img, 0, 250);
  lv_anim_start(&img);
}

void display_allpage_icons()
{
  lv_obj_clear_flag(img_charger, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_profile, LV_OBJ_FLAG_HIDDEN);
  // lv_obj_clear_flag(img_wifi, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_wifi5, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_wifi4, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_wifi3, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_wifi2, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_wifi1, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_signal1, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_signal2, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_signal3, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_signal4, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_signal5, LV_OBJ_FLAG_HIDDEN);
  // lv_obj_clear_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(label_time, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_location, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(label_location, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(header_rect, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(header_text, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(label_guest, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_plug, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(label_plug, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_health, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_cloud_connection, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_charger, LV_OBJ_FLAG_HIDDEN);
  lv_obj_clear_flag(img_footer, LV_OBJ_FLAG_HIDDEN);
}

///////////////// Deafault screen ///////////////////
void home_screen()
{
  display_allpage_icons();

  default_heading = lv_label_create(scr_home);
  lv_label_set_text(default_heading, "Charger Ready! Please Plug in to start Charging");
  lv_obj_align(default_heading, LV_ALIGN_CENTER, 0, -260);
  lv_obj_add_style(default_heading, &style_dc_ready, LV_STATE_DEFAULT);
}
