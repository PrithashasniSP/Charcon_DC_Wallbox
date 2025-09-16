/**
 * progress_page_nv.c
 *
 * Created on: 07-Dec-2023
 * Author: PSI2COB
 */

/* The file that controls the UI State */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "pthread.h"

#include "MQTTClient.h"
#include "controller.h"
#include "../view/launch_screen.h"
#include "../view/health_check.h"
#include "../view/device_detect.h"
#include "../view/progress_screen.h"
#include "../view/allpage_icons.h"
#include "../view/admin_page.h"
#include "../view/admin_access.h"
#include "../view/styles.h"
#include "../../sub.h"
#include "../../lvgl/lvgl.h"


void progress_admin_page()
{
    progress_page_hidden();
    if (header_page == CONST_AdminLoginPage)
    {
        if (user_flag != 0)
        {
            admin_login_pages();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_AdminLoginPage;
            user_flag = CONST_AdminLoginPage;
        }
        else
        {
            admin_login_pages();
            progress_page_hidden();
            prev_header_page = CONST_AdminLoginPage;
            user_flag = CONST_AdminLoginPage;
        }
    }
    else if (header_page == CONST_SoftwareUpdate)
    {
        if (user_flag != 0)
        {
            scr_software_update();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_SoftwareUpdate;
            user_flag = CONST_SoftwareUpdate;
        }
        else
        {
            scr_software_update();
            progress_page_hidden();
            prev_header_page = CONST_SoftwareUpdate;
            user_flag = CONST_SoftwareUpdate;
        }
    }
    else if (header_page == CONST_VseccSettings)
    {
        if (user_flag != 0)
        {
            scr_vsecc_settings();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_VseccSettings;
            user_flag = CONST_VseccSettings;
        }
        else
        {
            scr_vsecc_settings();
            progress_page_hidden();
            prev_header_page = CONST_VseccSettings;
            user_flag = CONST_VseccSettings;
        }
    }
    else if (header_page == CONST_CharconSettings)
    {
        if (user_flag != 0)
        {
            scr_charcon_settings();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_CharconSettings;
            user_flag = CONST_CharconSettings;
        }
        else
        {
            scr_charcon_settings();
            progress_page_hidden();
            prev_header_page = CONST_CharconSettings;
            user_flag = CONST_CharconSettings;
        }
    }
    else if (header_page == CONST_MasterControl)
    {
        if (user_flag != 0)
        {
            scr_master_control();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_MasterControl;
            user_flag = CONST_MasterControl;
        }
        else
        {
            scr_master_control();
            progress_page_hidden();
            prev_header_page = CONST_MasterControl;
            user_flag = CONST_MasterControl;
        }
    }
    else if (header_page == CONST_AdminLogsPage)
    {
        if (user_flag != 0)
        {
            scr_logs_page();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_AdminLogsPage;
            user_flag = CONST_AdminLogsPage;
        }
        else
        {
            scr_logs_page();
            progress_page_hidden();
            prev_header_page = CONST_AdminLogsPage;
            user_flag = CONST_AdminLogsPage;
        }
    }
    else if (header_page == CONST_WiFiPage)
    {
        if (user_flag != 0)
        {
            scr_wifi_page();
            delete_obj_on_headpage(user_flag);
            prev_header_page = CONST_WiFiPage;
            user_flag = CONST_WiFiPage;
        }
        else
        {
            scr_wifi_page();
            delete_objects_on_page(prev_page);
            prev_header_page = CONST_WiFiPage;
            user_flag = CONST_WiFiPage;
        }
    }
}


/* Hide Progress Page */
void progress_page_hidden()
{
    lv_obj_add_flag(img_money, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_costgrid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(img_power, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_energy, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_solar, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_grid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_total, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(text_time_charging, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(img_cost_unit, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(cost_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(solar_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(grid_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(img_tot_cost, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(total_cost_value, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(terminate_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(img_terminate, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(charging_complete, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(unplug_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(chart1, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(timer_label, LV_OBJ_FLAG_HIDDEN);
}

/* Admin to progress page callback */
void admin_to_progress()
{
    lv_obj_clear_flag(img_money, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_costgrid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_power, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_energy, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_solar, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_grid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_total, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_time_charging, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_cost_unit, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(cost_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(solar_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(grid_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_tot_cost, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(total_cost_value, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(chart1, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(timer_label, LV_OBJ_FLAG_HIDDEN);
}

/* Display Progress Page */
void progress_page_display()
{
    lv_obj_clear_flag(img_money, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_costgrid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_power, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_energy, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_solar, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_grid, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_total, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(text_time_charging, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_cost_unit, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(cost_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(solar_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(grid_energy_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(img_tot_cost, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(total_cost_value, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(stop_button, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(chart1, LV_OBJ_FLAG_HIDDEN);
    lv_obj_clear_flag(timer_label, LV_OBJ_FLAG_HIDDEN);
}

