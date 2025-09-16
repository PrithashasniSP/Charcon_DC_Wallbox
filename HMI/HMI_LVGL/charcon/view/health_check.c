/**
 * health_check.c
 *
 * Created on: 28-Aug-2023
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
#include "../../sub.h"

lv_obj_t *img_red_check;
lv_obj_t *img_green_check;
lv_obj_t *label_dc_text;
lv_obj_t *cable_text;
lv_obj_t *power_text;
lv_obj_t *check1_text;
lv_obj_t *check2_text;
lv_obj_t *ready_text;
lv_obj_t *green_heart;
lv_obj_t *img_plug_connect;
lv_obj_t *connection_text;
lv_obj_t *vehicle_text;
lv_obj_t *start_button;
lv_obj_t *start_charging;
lv_obj_t *start_text;
lv_obj_t *img_initializing;
lv_obj_t *initialize_text;
lv_obj_t *scr_check;
lv_obj_t *check1_good;
lv_obj_t *check2_good;
lv_obj_t *test_b1;
lv_obj_t *test_b2;

lv_timer_t *check_task;

/////////////////////////////////  Health Check Page ///////////////////////////////

void screen_dc_check()
{
    display_allpage_icons();

    img_red_check = lv_img_create(img_charger);
    lv_img_set_src(img_red_check, &red_check);
    lv_obj_align(img_red_check, LV_ALIGN_CENTER, 0, 0);

    label_dc_text = lv_label_create(scr_home);
    lv_label_set_text(label_dc_text, "Health Check in Progress...");
    lv_obj_align(label_dc_text, LV_ALIGN_CENTER, 0, -260);
    lv_obj_add_style(label_dc_text, &style_dc_text, LV_STATE_DEFAULT);

    cable_text = lv_label_create(scr_home);
    lv_label_set_text(cable_text, "Cable :");
    lv_obj_align(cable_text, LV_ALIGN_CENTER, -500, 0);
    lv_obj_add_style(cable_text, &style_check_text, LV_STATE_DEFAULT);

    power_text = lv_label_create(scr_home);
    lv_label_set_text(power_text, "Power Board :");
    lv_obj_align(power_text, LV_ALIGN_CENTER, -450, 90);
    lv_obj_add_style(power_text, &style_check_text, LV_STATE_DEFAULT);

    check1_text = lv_label_create(scr_home);
    lv_label_set_text(check1_text, "Check");
    lv_obj_align(check1_text, LV_ALIGN_CENTER, -380, 0);
    lv_obj_add_flag(check1_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_style(check1_text, &style_check_text, LV_STATE_DEFAULT);

    check1_good = lv_label_create(scr_home);
    lv_label_set_text(check1_good, "Good");
    lv_obj_add_flag(check1_good, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(check1_good, LV_ALIGN_CENTER, -380, 0);
    lv_obj_add_style(check1_good, &style_check_good, LV_STATE_DEFAULT);

    check2_text = lv_label_create(scr_home);
    lv_label_set_text(check2_text, "Check");
    lv_obj_align(check2_text, LV_ALIGN_CENTER, -290, 90);
    lv_obj_add_flag(check2_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_style(check2_text, &style_check_text, LV_STATE_DEFAULT);
    
    check2_good = lv_label_create(scr_home);
    lv_label_set_text(check2_good, "Good");
    lv_obj_align(check2_good, LV_ALIGN_CENTER, -290, 90);
    lv_obj_add_flag(check2_good, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_style(check2_good, &style_check_good, LV_STATE_DEFAULT);
    
    img_green_check = lv_img_create(img_charger);
    lv_img_set_src(img_green_check, &green_check);
    lv_obj_add_flag(img_green_check, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(img_green_check, LV_ALIGN_CENTER, 0, 0);

    ready_text = lv_label_create(scr_home);
    lv_label_set_text(ready_text, "Charger Ready! Please Plug in to start Charging");
    lv_obj_align(ready_text, LV_ALIGN_CENTER, 0, -260);
    lv_obj_add_flag(ready_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_style(ready_text, &style_dc_ready, LV_STATE_DEFAULT);

    /* Update MQTT values in LVGL*/
    check_task = lv_timer_create(cable_check_status, 1000, NULL);
    lv_timer_ready(check_task);
    lv_timer_handler();
    lv_timer_set_repeat_count(check_task, -1);
}

void anim_opacity_cb(void *var, int32_t v)
{
    lv_obj_set_style_opa(var, LV_OPA_COVER - v, 0);
}

void anim_zoom_cb(void *var, int32_t v)
{
    lv_img_set_zoom(var, v);
}

void cable_check_status()
{
    /////////////////// Cable Check Status //////////////////
    if (CableCheckStatus == 1)
    {
        lv_obj_add_flag(check1_good, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(check1_text, LV_OBJ_FLAG_HIDDEN);

        lv_anim_t anim_opacity1;
        lv_anim_init(&anim_opacity1);
        lv_anim_set_var(&anim_opacity1, check1_text);
        lv_anim_set_exec_cb(&anim_opacity1, anim_opacity_cb);
        lv_anim_set_time(&anim_opacity1, 1000); // Animation duration in milliseconds
        lv_anim_set_values(&anim_opacity1, LV_OPA_0, LV_OPA_COVER);
        lv_anim_set_repeat_count(&anim_opacity1, LV_ANIM_REPEAT_INFINITE);
        lv_anim_start(&anim_opacity1);
    }
    else if (CableCheckStatus == 2)
    {
        lv_obj_clear_flag(check1_good, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(check1_text, LV_OBJ_FLAG_HIDDEN);
    }

    /////////////////// Power Board Status //////////////////

    if (PowerBoardStatus == 1)
    {
        lv_obj_add_flag(check2_good, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(check2_text, LV_OBJ_FLAG_HIDDEN);

        lv_anim_t anim_opacity2;
        lv_anim_init(&anim_opacity2);
        lv_anim_set_var(&anim_opacity2, check2_text);
        lv_anim_set_exec_cb(&anim_opacity2, anim_opacity_cb);
        lv_anim_set_time(&anim_opacity2, 1000); // Animation duration in milliseconds
        lv_anim_set_values(&anim_opacity2, LV_OPA_0, LV_OPA_COVER);
        lv_anim_set_repeat_count(&anim_opacity2, LV_ANIM_REPEAT_INFINITE);
        lv_anim_start(&anim_opacity2);
    }
    else if (PowerBoardStatus == 2)
    {
        lv_obj_add_flag(check2_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(check2_good, LV_OBJ_FLAG_HIDDEN);
    }

    /////////////////// Heart beat Status //////////////////
    if (HeartBeatMsg == 0)
    {
        lv_anim_t anim_img;
        lv_anim_init(&anim_img);
        lv_anim_set_exec_cb(&anim_img, anim_zoom_cb);
        lv_anim_set_var(&anim_img, img_red_check);
        lv_anim_set_values(&anim_img, 250, 265);
        lv_anim_set_repeat_count(&anim_img, LV_ANIM_REPEAT_INFINITE);
        lv_anim_start(&anim_img);
    }
    else if (HeartBeatMsg == 1)
    {
        lv_obj_add_flag(img_red_check, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(label_dc_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(img_green_check, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(ready_text, LV_OBJ_FLAG_HIDDEN);
    }
}

////////////////////////     Device Iniatializing    ///////////////////////

void initialize_device()
{
    display_allpage_icons();

    img_initializing = lv_img_create(scr_home);
    lv_img_set_src(img_initializing, &img_loader);
    lv_obj_align(img_initializing, LV_ALIGN_CENTER, 0, 0);

    connection_text = lv_label_create(scr_home);
    lv_label_set_text(connection_text, "Connection Detected!");
    lv_obj_align(connection_text, LV_ALIGN_CENTER, 0, -260);
    lv_obj_add_style(connection_text, &style_dc_ready, LV_STATE_DEFAULT);

    initialize_text = lv_label_create(scr_home);
    lv_label_set_text(initialize_text, "Initializing Device...");
    lv_obj_align(initialize_text, LV_ALIGN_CENTER, 0, 120);
    lv_obj_add_style(initialize_text, &style_confg_text, LV_STATE_DEFAULT);

    lv_anim_t anim_loader;
    lv_anim_init(&anim_loader);
    lv_anim_set_exec_cb(&anim_loader, anim_rotate_cb);
    lv_anim_set_var(&anim_loader, img_initializing);
    lv_anim_set_time(&anim_loader, 2000); // Animation duration in milliseconds
    lv_anim_set_values(&anim_loader, 0, 3600);
    lv_anim_set_repeat_count(&anim_loader, LV_ANIM_REPEAT_INFINITE);
    lv_anim_start(&anim_loader);
}

void anim_rotate_cb(void *var, int32_t v)
{
    lv_img_set_angle(var, v);
}

void scr_chart()
{
    lv_obj_del(test_b2);
    lv_obj_del(initialize_text);
    lv_obj_del(img_initializing);
    lv_obj_del(connection_text);
    lv_anim_del(img_initializing, anim_rotate_cb);

    create_progress_screen();

}
