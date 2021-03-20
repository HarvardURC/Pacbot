#include "motors.hpp"
#include "pac_pins.hpp"

/* initialize the two motors on the PacBot */
//Motor *right_motor = new Motor(pacBot_pins["motor_speed_r"],
//			       pacBot_pins["motor_direction_r"]);
//Motor *left_motor = new Motor(pacBot_pins["motor_speed_l"], 
//			      pacBot_pins["motor_direction_l"]);
//

Motor *right_motor;
Motor *left_motor;
void initialize_motors(){
	right_motor = new Motor(pacBot_pins["motor_speed_r"],
				pacBot_pins["motor_direction_r"]);
	left_motor = new Motor(pacBot_pins["motor_speed_l"],
				pacBot_pins["motor_direction_l"]);
}
