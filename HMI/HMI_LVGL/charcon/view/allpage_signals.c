/**
 * allpage_signals.c
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
#include "admin_page.h"
#include "admin_access.h"
#include "../../sub.h"
#include "../controller/controller.h"
#include "../controller/progress_page_nav.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define GSM_FILE_PATH "/home/position.json"

// A simple JSON parser for the provided JSON structure
void parse_json(const char *json)
{
  // Find "position" key
  const char *pos_start = strstr(json, "\"position\":");

  if (pos_start)
  {
    char *pos_end = strstr(pos_start + 13, "\""); // Skip over opening double quote
    if (pos_end)
    {
      char *comma_pos = strstr(pos_end + 1, ","); // Find the following comma
      if (comma_pos)
      {
        // Extract the position string without quotes and trailing comma
        char position[100];
        strncpy(position, pos_start + 13, comma_pos - pos_start - 13);
        position[comma_pos - pos_start - 14] = '\0'; // Replace closing double quote with null terminator

        // Copy the extracted position string to the global variable
        strcpy(g_position, position);
      }
    }
  }

  // Find "latitude" key
  const char *lat_start = strstr(json, "\"latitude\":");
  sscanf(lat_start, "\"latitude\":%lf,", &g_latitude);

  // Find "longitude" key
  const char *lon_start = strstr(json, "\"longitude\":");
  sscanf(lon_start, "\"longitude\":%lf,", &g_longitude);

  // Find "GSMsignal" key
  const char *signal_start = strstr(json, "\"GSMsignal\":");
  sscanf(signal_start, "\"GSMsignal\":%d", &g_GSMsignal);
}

/* Get the location from GPS latitude longitude points */
int get_position()
{
  // Get the home directory path of the current user
  char *home = getenv("HOME");
  if (home == NULL)
  {
    fprintf(stderr, "Error getting home directory.\n");
    return 1;
  }

  // Construct the absolute path to the JSON file in the home directory
  char json_path[256];
  // snprintf(GSM_FILE_PATH, sizeof(GSM_FILE_PATH), "%s/position.json", home);

  // Open the JSON file
  FILE *file = fopen(GSM_FILE_PATH, "r");
  if (!file)
  {
    fprintf(stderr, "Error opening JSON file.\n");
    return 1;
  }

  // Read the JSON data from the file
  fseek(file, 0, SEEK_END);
  long file_size = ftell(file);
  fseek(file, 0, SEEK_SET);
  char *json_data = (char *)malloc(file_size);
  fread(json_data, 1, file_size, file);
  fclose(file);

  // Parse JSON data and store values in global variables
  // printf("%s", json_data);
  parse_json(json_data);

  /* Get location from the GPS Module and display */

  loc_text = lv_label_get_text(label_location);
  start = loc_text;
  while (*start != '\0')
  {
    char_count++;
    start++;
  }

  lv_label_set_text(label_location, g_position);

  // Free allocated memory
  free(json_data);

  return 0;
}

//////////////////////////// GSM Network Signal ////////////////////////////////////
void get_gsm_signal()
{
  if (g_GSMsignal == 0)
  {
    lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
  else if (g_GSMsignal == 1)
  {
    lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
  else if (g_GSMsignal == 2)
  {
    lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
  else if (g_GSMsignal == 3)
  {
    lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
  else if (g_GSMsignal == 4)
  {
    lv_obj_add_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
  else
  {
    lv_obj_clear_flag(img_no_signal, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_signal1, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal2, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_signal5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_signal5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
}

//////////////////////////// Wifi signal ////////////////////////////////
void get_wifi_signal()
{
  if (Wifisignal == 0)
  {
    lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }

  else if (Wifisignal == 1)
  {
    lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }

  else if (Wifisignal == 2)
  {
    lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }

  else if (Wifisignal == 3)
  {
    lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }

  else if (Wifisignal == 4)
  {
    lv_obj_add_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, LV_COLOR_WHITE, LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }

  else
  {
    lv_obj_clear_flag(img_no_wifi, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_style_img_recolor(img_wifi1, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi1, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi2, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi2, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi3, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi3, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi4, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi4, LV_OPA_COVER, LV_STATE_DEFAULT);

    lv_obj_set_style_img_recolor(img_wifi5, lv_color_hex(0x3A3A3A), LV_STATE_DEFAULT);
    lv_obj_set_style_img_recolor_opa(img_wifi5, LV_OPA_COVER, LV_STATE_DEFAULT);
  }
}