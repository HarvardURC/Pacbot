#include "motors.hpp"
#include "pac_pins.hpp"

/* initialize the two motors on the PacBot */
Motors::Motors() {
    printf("Initializing Motors\n");
    this->right_motor = new Motor(pacBot_pins["motor_speed_r"],
                                  pacBot_pins["motor_direction_r"]);
    printf("right motor iniailized\n");
    this->left_motor = new Motor(pacBot_pins["motor_speed_l"],
                                 pacBot_pins["motor_direction_l"]);
    printf("Motors Initialized Successfully\n");
}

Motors motors = Motors();