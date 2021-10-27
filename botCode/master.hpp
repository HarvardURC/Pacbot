// This file will run on loop and control the robot

#ifndef MASTER_H
#define MASTER_H

#include "utils/conversions.hpp"

const double TICK_LENGTH = millis_to_secs(20);

static void start();

#endif