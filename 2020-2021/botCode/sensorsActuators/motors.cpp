#include "motors.hpp"
#include "pac_pins.hpp"
#include <thread>
#include <stdio.h>

/* initialize the two motors on the PacBot */
//Motor *right_motor = new Motor(pacBot_pins["motor_speed_r"],
//			       pacBot_pins["motor_direction_r"]);
//Motor *left_motor = new Motor(pacBot_pins["motor_speed_l"], 
//			      pacBot_pins["motor_direction_l"]);
//

Motor *right_motor;
Motor *left_motor;

void initialize_motors(){
	using namespace std::chrono_literals;
	right_motor = new Motor(pacBot_pins["motor_speed_r"],
				pacBot_pins["motor_direction_r"]);
	printf("Initialized right motor: %p\n", right_motor);
	std::this_thread::sleep_for(1000ms);
	left_motor = new Motor(pacBot_pins["motor_speed_l"],
				pacBot_pins["motor_direction_l"]);
	printf("Initialized left motor: %p\n", left_motor);
}
