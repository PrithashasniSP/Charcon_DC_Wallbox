cmake_minimum_required(VERSION 3.1)

project(charcon-lvgl-wl)

include_directories(.)
add_subdirectory(lvgl)
add_subdirectory(lv_drivers)

# Add the paho.mqtt.c library as a subdirectory
add_subdirectory(paho.mqtt.c)

file(GLOB_RECURSE INCLUDES "lv_drivers/*.h" "lv_demos/*.h"  "lvgl/*.h" "charcon/view/*.h" "charcon/controller/*.h" "./*.h" )
file(GLOB_RECURSE SOURCES  "lv_drivers/*.c" "lv_demos/*.c"  "lvgl/*.c" "charcon/assets/*.c" "charcon/view/*.c" "charcon/controller/*.c")

SET(CMAKE_CXX_FLAGS "-O3")
add_executable(${PROJECT_NAME} main.c sub.c ${SOURCES} ${INCLUDES})
target_link_libraries(${PROJECT_NAME} PRIVATE lvgl lvgl::examples lvgl::demos
	lvgl::drivers wayland-client wayland-cursor xkbcommon paho-mqtt3c)
install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)
