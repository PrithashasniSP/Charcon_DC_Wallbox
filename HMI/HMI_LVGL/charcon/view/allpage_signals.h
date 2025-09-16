/**
 * allpage_signals.h
 *
 * Created on: 07-Dec-2023
 * Author: PSI2COB
 */

#ifndef _ALLPAGE_SIGNALS_H_
#define _ALLPAGE_SIGNALS_H_

/* System Includes*/
#include <stdio.h>
#include <time.h>
#include "../../lvgl/lvgl.h"

extern int get_position();
extern void get_gsm_signal();
extern void get_wifi_signal();
extern void parse_json(const char *json);

#endif