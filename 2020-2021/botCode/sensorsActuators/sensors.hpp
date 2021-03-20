#ifndef SENSORS_H
#define SENSORS_H

#include "./sa_interface/tofsensor.hpp"

/* PacBot specific sensors */

extern TofSensor *front_tof;
extern TofSensor *rear_tof;
extern TofSensor *left_tof;
extern TofSensor *right_tof;

void initialize_sensors();


#endif
