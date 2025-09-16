/**
 * progress_check.c
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#include <unistd.h>
#include "../../lvgl/lvgl.h"
#include "../controller/controller.h"
#include "health_check.h"
#include "styles.h"
#include "launch_screen.h"
#include "progress_screen.h"
#include "colors.h"
#include "allpage_icons.h"
#include "admin_access.h"
#include "../../sub.h"
#include "pub_mqtt.h"

/*Project Includes*/
lv_obj_t *img_money;
lv_obj_t *img_power;
lv_obj_t *chart1;
lv_obj_t *text_costgrid;
lv_obj_t *text_energy;
lv_obj_t *text_total;
lv_obj_t *stop_button;
lv_obj_t *stop_charging;
lv_obj_t *stop_text;
lv_obj_t *text_solar;
lv_obj_t *text_grid;
lv_obj_t *text_time_charging;
lv_obj_t *cost_text;
lv_obj_t *solar_energy_text;
lv_obj_t *grid_energy_text;
lv_obj_t *total_cost_value;
lv_obj_t *terminate_text;
lv_obj_t *charging_complete;
lv_obj_t *unplug_text;
lv_obj_t *timer_label;
lv_obj_t *img_terminate;
lv_obj_t *img_cost_unit;
lv_obj_t *img_tot_cost;

lv_timer_t *timer_task;
lv_timer_t *progress_task;

//////// Physical values ///////////
int sec = 0, min = 0, hr = 0;
char cost_on_grid[10] = "0.41";

/////////// Chart values //////////
lv_chart_series_t *ser1;
lv_chart_series_t *ser2;

void create_progress_screen()
{
    img_money = lv_img_create(scr_home);
    lv_img_set_src(img_money, &icon_money);
    lv_obj_add_flag(img_money, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(img_money, LV_ALIGN_TOP_LEFT, 18, 100);

    text_costgrid = lv_label_create(scr_home);
    lv_obj_add_flag(text_costgrid, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(text_costgrid, "Cost on Grid per kWh:");
    lv_obj_align(text_costgrid, LV_ALIGN_TOP_LEFT, 110, 100);
    lv_obj_add_style(text_costgrid, &style_check_text, LV_STATE_DEFAULT);

    img_power = lv_img_create(scr_home);
    lv_img_set_src(img_power, &icon_power);
    lv_obj_add_flag(img_power, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(img_power, LV_ALIGN_TOP_LEFT, 5, 210);

    text_energy = lv_label_create(scr_home);
    lv_obj_add_flag(text_energy, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(text_energy, "Energy Consumed:");
    lv_obj_align(text_energy, LV_ALIGN_TOP_LEFT, 110, 215);
    lv_obj_add_style(text_energy, &style_check_text, LV_STATE_DEFAULT);

    text_solar = lv_label_create(scr_home);
    lv_label_set_text(text_solar, "Solar");
    lv_obj_add_flag(text_solar, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(text_solar, LV_ALIGN_TOP_LEFT, 110, 290);
    lv_obj_add_style(text_solar, &style_check_text, LV_STATE_DEFAULT);

    text_grid = lv_label_create(scr_home);
    lv_label_set_text(text_grid, "Grid");
    lv_obj_add_flag(text_grid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(text_grid, LV_ALIGN_LEFT_MID, 110, -25);
    lv_obj_add_style(text_grid, &style_check_text, LV_STATE_DEFAULT);

    text_total = lv_label_create(scr_home);
    lv_obj_add_flag(text_total, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(text_total, "Total Cost of Charging:");
    lv_obj_align(text_total, LV_ALIGN_LEFT_MID, 30, 60);
    lv_obj_add_style(text_total, &style_check_text, LV_STATE_DEFAULT);

    text_time_charging = lv_label_create(scr_home);
    lv_obj_add_flag(text_time_charging, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(text_time_charging, "Time since Charging Start");
    lv_obj_align(text_time_charging, LV_ALIGN_BOTTOM_RIGHT, -100, -140);
    lv_obj_add_style(text_time_charging, &style_check_text, LV_STATE_DEFAULT);

    ////////////////// Physical values ////////////////////
    img_cost_unit = lv_img_create(scr_home);
    lv_img_set_src(img_cost_unit, &img_cost);
    lv_obj_add_flag(img_cost_unit, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(img_cost_unit, LV_ALIGN_TOP_LEFT, 110, 138);

    cost_text = lv_label_create(scr_home);
    lv_obj_align(cost_text, LV_ALIGN_TOP_LEFT, 140, 140);
    lv_obj_add_flag(cost_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_style(cost_text, &style_vehicle_text, LV_STATE_DEFAULT);

    solar_energy_text = lv_label_create(scr_home);
    lv_obj_add_flag(solar_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text_fmt(solar_energy_text, "%.f kWh", SolarEnergy);
    lv_obj_align(solar_energy_text, LV_ALIGN_TOP_LEFT, 230, 290);
    lv_obj_add_style(solar_energy_text, &style_yellow_text, LV_STATE_DEFAULT);

    grid_energy_text = lv_label_create(scr_home);
    lv_obj_add_flag(grid_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text_fmt(grid_energy_text, "%.f kWh", GridEnergy);
    lv_obj_align(grid_energy_text, LV_ALIGN_LEFT_MID, 230, -25);
    lv_obj_add_style(grid_energy_text, &style_blue_text, LV_STATE_DEFAULT);

    img_tot_cost = lv_img_create(scr_home);
    lv_img_set_src(img_tot_cost, &img_tot);
    lv_obj_add_flag(img_tot_cost, LV_OBJ_FLAG_HIDDEN);
    lv_obj_set_style_img_recolor(img_tot_cost, lv_color_hex(0xf8b484), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_tot_cost, LV_OPA_COVER, LV_STATE_DEFAULT);
    lv_obj_align(img_tot_cost, LV_ALIGN_LEFT_MID, 30, 112);

    total_cost_value = lv_label_create(scr_home);
    lv_obj_add_flag(total_cost_value, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text_fmt(total_cost_value, "%.f", TotCost);
    lv_obj_align(total_cost_value, LV_ALIGN_LEFT_MID, 70, 110);
    lv_obj_add_style(total_cost_value, &style_total_text, LV_STATE_DEFAULT);

    ////////////// Charging state ////////////////////
    stop_button = lv_btn_create(scr_home);
    lv_obj_set_size(stop_button, 150, 90);
    lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(stop_button, LV_ALIGN_BOTTOM_LEFT, 30, -90);
    lv_obj_add_style(stop_button, &style_stop_button, LV_STATE_DEFAULT);
    lv_obj_add_event_cb(stop_button, pub_stop, LV_EVENT_CLICKED, NULL);

    stop_text = lv_label_create(stop_button);
    lv_label_set_text(stop_text, "STOP");
    lv_obj_align(stop_text, LV_ALIGN_CENTER, 0, 0);
    lv_obj_add_style(stop_text, &style_stop_text, LV_STATE_DEFAULT);

    terminate_text = lv_label_create(scr_home);
    lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(terminate_text, "Terminating Charging Session");
    lv_obj_align(terminate_text, LV_ALIGN_BOTTOM_LEFT, 30, -110);
    lv_obj_add_style(terminate_text, &style_terminate_text, LV_STATE_DEFAULT);

    img_terminate = lv_img_create(scr_home);
    lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);
    lv_img_set_src(img_terminate, &img_loader);
    lv_obj_align(img_terminate, LV_ALIGN_BOTTOM_MID, 45, -50);
    lv_img_set_zoom(img_terminate, 120);
    lv_obj_set_style_img_recolor(img_terminate, LV_COLOR_RED, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_terminate, LV_OPA_COVER, LV_STATE_DEFAULT);

    charging_complete = lv_label_create(scr_home);
    lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(charging_complete, "Charging Complete!");
    lv_obj_align(charging_complete, LV_ALIGN_BOTTOM_LEFT, 30, -145);
    lv_obj_add_style(charging_complete, &style_green_text, LV_STATE_DEFAULT);

    unplug_text = lv_label_create(scr_home);
    lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text(unplug_text, "Please unplug the charger");
    lv_obj_align(unplug_text, LV_ALIGN_BOTTOM_LEFT, 30, -100);
    lv_obj_add_style(unplug_text, &style_white_text, LV_STATE_DEFAULT);

    /////////////// Progress chart ////////////////////
    chart1 = lv_chart_create(scr_home);
    lv_obj_set_size(chart1, 500, 450);
    lv_obj_add_flag(chart1, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(chart1, LV_ALIGN_RIGHT_MID, -100, -50);
    lv_chart_set_type(chart1, LV_CHART_TYPE_LINE);
    lv_chart_set_div_line_count(chart1, 6, 5);
    lv_obj_set_style_bg_opa(chart1, LV_OPA_30, LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(chart1, LV_COLOR_BLACK, LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(chart1, LV_COLOR_GREY, LV_STATE_DEFAULT);
    lv_obj_add_event_cb(chart1, draw_event_cb, LV_EVENT_DRAW_PART_BEGIN, NULL);
    lv_obj_set_style_line_color(chart1, LV_COLOR_GREY, LV_PART_MAIN | LV_STATE_DEFAULT);

    // /* Set range to 0 to 100 for percentages. Draw ticks */
    lv_chart_set_range(chart1, LV_CHART_AXIS_PRIMARY_Y, 0, 4000);
    lv_chart_set_axis_tick(chart1, LV_CHART_AXIS_PRIMARY_Y, 3, 0, 5, 1, true, 500);
    // lv_chart_set_range(chart1, LV_CHART_AXIS_PRIMARY_X, 0, 200);
    // lv_chart_set_axis_tick(chart1, LV_CHART_AXIS_PRIMARY_X, 5, 5, 5, 1, true, 30);
    lv_obj_set_style_size(chart1, 0, LV_PART_INDICATOR);

    /*Add two data series*/
    ser1 = lv_chart_add_series(chart1, lv_color_hex(0xf9c459), LV_CHART_AXIS_PRIMARY_Y);
    ser2 = lv_chart_add_series(chart1, lv_color_hex(0x44b6ce), LV_CHART_AXIS_PRIMARY_Y);
    lv_chart_set_point_count(chart1, 50);

    /* Start the timer*/
    sec = 0;
    min = 0;
    hr = 0;

    timer_label = lv_label_create(scr_home);
    lv_obj_add_flag(timer_label, LV_OBJ_FLAG_HIDDEN);
    lv_label_set_text_fmt(timer_label, "%02dh  %02dm  %02ds", hr, min, sec);
    lv_obj_align(timer_label, LV_ALIGN_BOTTOM_RIGHT, -100, -95);
    lv_obj_add_style(timer_label, &style_white_text, LV_STATE_DEFAULT);
}

void pub_stop(lv_event_t *event)
{
    for (int i = 0; i < 10; i++)
    {
        if (StopEventAck != 1)
        {
            pub_main();
            sleep(2);
        }
    }
}

void create_progress_chart()
{
    if (cost_on_grid != NULL)
    {
        lv_label_set_text(cost_text, cost_on_grid);
    }

    if (SolarEnergy != 0)
    {
        lv_label_set_text_fmt(solar_energy_text, "%.3f kWh", SolarEnergy);
    }
    if (GridEnergy != 0)
    {
        lv_label_set_text_fmt(grid_energy_text, "%.3f kWh", GridEnergy);
    }
    if (TotCost != 0)
    {
        lv_label_set_text_fmt(total_cost_value, "%.3f", TotCost);
    }

    if (ySolarPwr != 0 || yGridPwr != 0)
    {

        lv_chart_set_next_value(chart1, ser1, ySolarPwr + yGridPwr);

        lv_chart_set_next_value(chart1, ser2, yGridPwr);

        lv_chart_refresh(chart1);
    }

    /////// Charging progress state ///////
    charging_progress_state();
}

static void draw_event_cb(lv_event_t *e)
{
    lv_obj_t *obj = lv_event_get_target(e);

    /*Add the faded area before the lines are drawn*/
    lv_obj_draw_part_dsc_t *dsc = lv_event_get_draw_part_dsc(e);
    if (dsc->part == LV_PART_ITEMS)
    {
        if (!dsc->p1 || !dsc->p2)
            return;

        /*Add a line mask that keeps the area below the line*/
        lv_draw_mask_line_param_t line_mask_param;
        lv_draw_mask_line_points_init(&line_mask_param, dsc->p1->x, dsc->p1->y, dsc->p2->x, dsc->p2->y, LV_DRAW_MASK_LINE_SIDE_BOTTOM);
        int16_t line_mask_id = lv_draw_mask_add(&line_mask_param, NULL);

        /*Draw a rectangle that will be affected by the mask*/
        lv_draw_rect_dsc_t draw_rect_dsc;
        lv_draw_rect_dsc_init(&draw_rect_dsc);
        draw_rect_dsc.bg_opa = LV_OPA_COVER;
        draw_rect_dsc.bg_color = dsc->line_dsc->color;

        lv_area_t a;
        a.x1 = dsc->p1->x;
        a.x2 = dsc->p2->x;
        a.y1 = LV_MIN(dsc->p1->y, dsc->p2->y);
        a.y2 = obj->coords.y2 -
               13; /* -13 cuts off where the rectangle draws over the chart margin. Without this an area of 0 doesn't look like 0 */
        lv_draw_rect(dsc->draw_ctx, &draw_rect_dsc, &a);

        /*Remove the mask*/
        lv_draw_mask_free_param(&line_mask_param);
        lv_draw_mask_remove_id(line_mask_id);
    }
}

//////////////////////// Charging Progress Page ///////////////////////////

void charging_progress_state()
{
    if (ChargingState == 0)
    {
        lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);

        ////// Start the timer /////
        charge_timer_start();
        
        if (admin_flag != 0)
        {
            lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
        }
    }

    else if (ChargingState == 1)
    {
        lv_obj_clear_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);

        lv_anim_t anim_loader;
        lv_anim_init(&anim_loader);
        lv_anim_set_var(&anim_loader, img_terminate);
        lv_anim_set_exec_cb(&anim_loader, anim_rotate_cb);
        lv_anim_set_time(&anim_loader, 2000); // Animation duration in milliseconds
        lv_anim_set_values(&anim_loader, 0, 3600);
        lv_anim_set_repeat_count(&anim_loader, LV_ANIM_REPEAT_INFINITE);
        lv_anim_start(&anim_loader);

        if (admin_flag != 0)
        {
            lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
            lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);
        }
    }

    else if (ChargingState == 2)
    {
        lv_obj_clear_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);

        if (admin_flag != 0)
        {
            lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
            lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
        }
    }
    else if (ChargingState == 3)
    {
        lv_label_set_text(charging_complete, "Connector Unplugged!");

        lv_label_set_text(unplug_text, "Charging session info updated to Cloud");

        lv_obj_clear_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);

        if (admin_flag != 0)
        {
            lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
            lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
        }
    }
}

///////////////////////////////// Charging Timer ///////////////////////////////////

void charge_timer_start()
{
    lv_label_set_text_fmt(timer_label, "%02dh  %02dm  %02ds", hr, min, sec);

    sec++;
    if (sec >= 60)
    {
        sec = 0;
        min++;
        if (min >= 60)
        {
            min = 0;
            hr++;
            if (hr >= 24)
            {
                hr = 0;
            }
        }
    }
}