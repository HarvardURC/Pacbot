#ifndef _MOVEMENT_H_
#define _MOVEMENT_H_

#include "vl6180_pi.h"
#include "state.h"
#include "pacbot_direction.h"

#define RIGHT_MAX 99;
#define LEFT_MAX 100;


void go_straight();
void correct_rot();
void left_add_count();
void initialise_irs();
void turn_right();
void turn_left();
void turn_around();
void forward_half();
void setupMovement();
void all_init();

#endif /* _MOVEMENT_H_*/
