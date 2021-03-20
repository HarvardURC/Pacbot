#ifndef MOTORS_H
#define MOTORS_H

#include "./sa_interface/motor.hpp"

/* PacBot specific motors */
extern Motor *right_motor;
extern Motor *left_motor;

void initialize_motors();
#endif
