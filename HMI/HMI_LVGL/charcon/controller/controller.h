/**
 * controller.h
 *
 * Created on: 28-Aug-2023
 * Author: PSI2COB
 */

#ifndef _CONTROLLER_H_
#define _CONTROLLER_H_

#include "../../lvgl/lvgl.h"

extern void ui_start();
extern void page_change();
extern void admin_change();
extern void admin_page();
extern void wallbox_page();
extern void progress_page_timer();
extern void admin_before_progress();

extern void delete_objects_on_page(int page);
extern void delete_obj_on_headpage(int header_page);

extern lv_timer_t *page_task;
extern lv_timer_t *admin_task;
extern int header_page;
extern int prev_header_page;
extern int prev_page;
extern int user_flag;
extern int prog_flag;
extern int admin_flag;

#endif //_CONTROLLER_H_