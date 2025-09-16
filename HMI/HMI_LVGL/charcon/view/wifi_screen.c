/**
 * wifi_screen.c
 *
 * Created on: 07-Dec-2023
 * Author: PSI2COB
 */

#include "../../lvgl/lvgl.h"
#include "health_check.h"
#include "styles.h"
#include "launch_screen.h"
#include "progress_screen.h"
#include "colors.h"
#include "allpage_icons.h"
#include "allpage_signals.h"
#include "device_detect.h"
#include "admin_page.h"
#include "admin_access.h"
#include "wifi_screen.h"

lv_obj_t *back_icon;
lv_obj_t *wifi_text;
lv_obj_t *network_bg;
lv_obj_t *no_wifi_text;
lv_obj_t *no_wifi_icon;
lv_obj_t *wifi_ta;
lv_obj_t *wifi_pwd;
lv_obj_t *inc_text;
lv_obj_t *wifi_keyboard;
lv_obj_t *user_name;
lv_obj_t *wf_pwd;

typedef struct {
    const char *Username;
    const char *Password;
} WifiCredentials;

void scr_wifi_page()
{
    display_allpage_icons();
    lv_obj_add_flag(img_charger, LV_OBJ_FLAG_HIDDEN);

    back_icon = lv_img_create(scr_home);
    lv_img_set_src(back_icon, &cancel_icon);
    lv_img_set_zoom(back_icon, 180);
    lv_obj_align(back_icon, LV_ALIGN_TOP_LEFT, 25, 88);
    lv_obj_add_flag(back_icon, LV_OBJ_FLAG_CLICKABLE);
    lv_obj_add_event_cb(back_icon, prev_screen_cb, LV_EVENT_CLICKED, NULL);

    wifi_text = lv_label_create(scr_home);
    lv_label_set_text(wifi_text, "Wi-Fi");
    lv_obj_align(wifi_text, LV_ALIGN_TOP_LEFT, 90, 95);
    lv_obj_set_style_text_color(wifi_text, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(wifi_text, &lv_font_montserrat_34, LV_STATE_DEFAULT);

    user_name = lv_label_create(scr_home);
    lv_label_set_text(user_name, "Username");
    lv_obj_align(user_name, LV_ALIGN_TOP_LEFT, 40, 260);
    lv_obj_add_style(user_name, &style_check_text, LV_STATE_DEFAULT);

    wf_pwd = lv_label_create(scr_home);
    lv_label_set_text(wf_pwd, "Password");
    lv_obj_align(wf_pwd, LV_ALIGN_TOP_LEFT, 40, 350);
    lv_obj_add_style(wf_pwd, &style_check_text, LV_STATE_DEFAULT);

    wifi_ta = lv_textarea_create(scr_home);
    lv_obj_set_size(wifi_ta, 350, 150);
    lv_obj_align(wifi_ta, LV_ALIGN_TOP_LEFT, 220, 250);
    lv_textarea_set_one_line(wifi_ta, true);
    lv_textarea_set_password_mode(wifi_ta, false);
    lv_textarea_set_max_length(wifi_ta, 10);
    lv_obj_add_style(wifi_ta, &style_textbox, LV_PART_MAIN);
    lv_obj_add_event_cb(wifi_ta, wifi_ta_event, LV_EVENT_ALL, NULL);

    //// Password box
    wifi_pwd = lv_textarea_create(scr_home);
    lv_obj_set_size(wifi_pwd, 350, 150);
    lv_obj_align(wifi_pwd, LV_ALIGN_TOP_LEFT, 220, 340);
    lv_textarea_set_text(wifi_pwd, "");
    lv_textarea_set_password_mode(wifi_pwd, true);
    lv_textarea_set_one_line(wifi_pwd, true);
    lv_textarea_set_max_length(wifi_pwd, 10);
    lv_obj_add_style(wifi_pwd, &style_textbox, LV_PART_MAIN);
    lv_obj_add_event_cb(wifi_pwd, wifi_ta_event, LV_EVENT_ALL, NULL);

    wifi_keyboard = lv_keyboard_create(scr_home);
    lv_obj_clear_flag(wifi_keyboard, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_size(wifi_keyboard, 600, 300);
    lv_obj_align(wifi_keyboard, LV_ALIGN_RIGHT_MID, -30, 10);
    lv_keyboard_set_textarea(wifi_keyboard, wifi_ta); /*Focus it on one of the text areas to start*/
    lv_obj_add_style(wifi_keyboard, &style_keyboard, LV_PART_MAIN);
    lv_obj_add_style(wifi_keyboard, &style_keyboard_btn, LV_PART_ITEMS);

    inc_text = lv_label_create(scr_home);
    lv_label_set_text(inc_text, "Incorrect username or password");
    lv_obj_add_flag(inc_text, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align_to(inc_text, wifi_pwd, LV_ALIGN_OUT_BOTTOM_MID, -140, 20);
    lv_obj_add_style(inc_text, &style_red_text, LV_STATE_DEFAULT);

    // network_bg = lv_obj_create(scr_home);
    // lv_obj_set_size(network_bg, 800, 500);
    // lv_obj_align(network_bg, LV_ALIGN_TOP_LEFT, 30, 150);
    // lv_obj_set_style_bg_color(network_bg, LV_COLOR_DARK_GREY, LV_STATE_DEFAULT);
    // lv_obj_set_style_border_color(network_bg, LV_COLOR_DARK_GREY, LV_STATE_DEFAULT);
    // lv_obj_set_style_bg_opa(network_bg, LV_OPA_90, LV_STATE_DEFAULT);

    // no_wifi_icon = lv_img_create(scr_home);
    // lv_img_set_src(no_wifi_icon, &no_wifi);
    // lv_img_set_zoom(no_wifi_icon, 230);
    // // lv_obj_set_style_bg_img_opa(no_wifi_icon, LV_OPA_80, LV_STATE_DEFAULT);
    // lv_obj_align(no_wifi_icon, LV_ALIGN_CENTER, 0, 70);

    // no_wifi_text = lv_label_create(scr_home);
    // lv_label_set_text(no_wifi_text, "No Wi-Fi networks");
    // lv_obj_align(no_wifi_text, LV_ALIGN_CENTER, 0, 130);
    // lv_obj_set_style_text_color(no_wifi_text, lv_color_hex(0x6c6c6c), LV_STATE_DEFAULT);
    // lv_obj_set_style_text_font(no_wifi_text, &lv_font_montserrat_28, LV_STATE_DEFAULT);
}

static void wifi_ta_event(lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    lv_obj_t *ta = lv_event_get_target(e);
    if (code == LV_EVENT_CLICKED || code == LV_EVENT_FOCUSED)
    {
        /*Focus on the clicked text area*/
        if (wifi_keyboard != NULL)
            lv_keyboard_set_textarea(wifi_keyboard, ta);
    }

    if (code == LV_EVENT_READY)
    {
        const char *username = lv_textarea_get_text(wifi_ta);
        const char *password = lv_textarea_get_text(wifi_pwd);

        save_wifi_credentials(username, password);
    }
}

void save_wifi_credentials(const char *username, const char *password) 
{
    FILE *file = fopen("/home/wifi.json", "w");
    if (file) {
        WifiCredentials creds;
        creds.Username = username;
        creds.Password = password;

        fprintf(file, "{\"Username\": \"%s\",\n\"Password\": \"%s\"}\n", creds.Username, creds.Password);
        fclose(file);
        printf("Wi-Fi credentials saved to wifi.json\n");
    } else {
        printf("Error opening wifi.json for writing\n");
    }
}