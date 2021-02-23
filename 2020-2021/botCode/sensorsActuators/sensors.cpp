#include "sensors.hpp"
#include "pac_pins.hpp"
#include "unistd.h"
#include "wiringPi.h"
#include <stdio.h>
#include <thread>

/* initialize all four sensors on the PacBot */
Sensors::Sensors() {
    std::this_thread::sleep_for(500ms);
    int all_pins[4] = {pacBot_pins["tof_front"], pacBot_pins["tof_left"],
                       pacBot_pins["tof_right"], pacBot_pins["tof_rear"]};

    // before initializing each sensor, ensure that all sensors are shutdown
    for (int i = 0; i < 4; i++) {
        pinMode(all_pins[i], OUTPUT);
        digitalWrite(all_pins[i], LOW);
        std::this_thread::sleep_for(500ms);
    }
    printf("Setting up front TOF sensor...\n");
    this->front_tof = new TofSensor(pacBot_pins["tof_front"], "front", 0x30);
    printf("Setting up left TOF sensor...\n");
    this->left_tof = new TofSensor(pacBot_pins["tof_left"], "left", 0x31);
    printf("Setting up right TOF sensor...\n");
    this->right_tof = new TofSensor(pacBot_pins["tof_right"], "right", 0x32);
    printf("Setting up rear TOF sensor...\n");
    this->rear_tof = new TofSensor(pacBot_pins["tof_rear"], "rear", 0x33);

    // Ensure we can receive distances from sensors
    int dist = this->front->distance();
    dist = this->rear->distance();
    dist = this->left->distance();
    dist = this->right->distance();
    (void)dist;
    printf("All sensors set up correctly!\n");
}
