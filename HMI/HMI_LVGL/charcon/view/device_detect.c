/**
 * device_detect.c
 *
 * Created on: 11-Sep-2023
 * Author: PSI2COB
 */

#include "../../lvgl/lvgl.h"
#include "health_check.h"
#include "styles.h"
#include "launch_screen.h"
#include "progress_screen.h"
#include "colors.h"
#include "allpage_icons.h"
#include "device_detect.h"
#include "../controller/controller.h"

lv_obj_t *scr_wallbox;
lv_obj_t *scr_failure;
lv_obj_t *img_failure;
lv_obj_t *img_heart_failure;
lv_obj_t *img_heart_conf;
lv_obj_t *failure_label;
lv_obj_t *configure_label;
lv_obj_t *please_conf;
lv_obj_t *service_label;
lv_obj_t *img_error;

LV_IMG_DECLARE(error_icon)

void wallbox_failure_status()
{
    if(header_flag != 0)
    {
        header_icons_close();
    }
    
    display_allpage_icons();
    lv_obj_clear_flag(header_rect, LV_OBJ_FLAG_CLICKABLE);
    lv_obj_clear_flag(label_guest, LV_OBJ_FLAG_CLICKABLE);

    failure_label = lv_label_create(scr_home);
    lv_label_set_text(failure_label, "Wall Box Failure Detected");
    lv_obj_align(failure_label, LV_ALIGN_CENTER, 0, -270);
    lv_obj_add_style(failure_label, &style_failure_text, LV_STATE_DEFAULT);

    service_label = lv_label_create(scr_home);
    lv_label_set_text(service_label, "Call Service Center");
    lv_obj_align(service_label, LV_ALIGN_CENTER, 0, 235);
    lv_obj_add_style(service_label, &style_failure_text, LV_STATE_DEFAULT);

    img_failure = lv_img_create(img_charger);
    lv_img_set_src(img_failure, &error_icon);
    lv_obj_align(img_failure, LV_ALIGN_CENTER, 0, 0);

}

void wallbox_not_configured()
{
    display_allpage_icons();

    configure_label = lv_label_create(scr_home);
    lv_label_set_text(configure_label, "Charger not Configured!");
    lv_obj_align(configure_label, LV_ALIGN_CENTER, 0, -270);
    lv_obj_add_style(configure_label, &style_confg_text, LV_STATE_DEFAULT);

    please_conf = lv_label_create(scr_home);
    lv_label_set_text(please_conf, "Please Configure the Charger");
    lv_obj_align(please_conf, LV_ALIGN_CENTER, 0, 235);
    lv_obj_add_style(please_conf, &style_confg_text, LV_STATE_DEFAULT);

    img_error = lv_img_create(img_charger);
    lv_img_set_src(img_error, &error_icon);
    lv_obj_align(img_error, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_img_recolor(img_error, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_error, LV_OPA_COVER, LV_STATE_DEFAULT);

}