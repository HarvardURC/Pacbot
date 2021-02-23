#ifndef SENSORS_H
#define SENSORS_H

#include "./sa_interface/tofsensor.hpp"

/* PacBot specific sensors */
class Sensors {
  public:
    Sensors();
    TofSensor *front_tof;
    TofSensor *rear_tof;
    TofSensor *left_tof;
    TofSensor *right_tof;
};

#endif
