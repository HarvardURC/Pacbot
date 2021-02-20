#include "motor.hpp"
#include "../pac_pins.cpp"
#include <string>
#include <iostream>
#include <unistd.h>

// Wiring pi needs to be setup at the start of the program!
extern "C" {
    #include <wiringPi.h>
}

using namespace std;

int main(void){
    wiringPiSetup();
    cout << pacBot_pins["motor_speed_l"] << endl;

    Motor left_motor = Motor(pacBot_pins["motor_speed_l"], pacBot_pins["motor_direction_l"]);
    Motor right_motor = Motor(pacBot_pins["motor_speed_r"], pacBot_pins["motor_direction_r"]);

    cout << "Motors Initialized." << endl;

    left_motor.move(BACKWARD, 50);
    sleep(1);
    left_motor.stop();
    left_motor.move(FORWARD, 50);
    sleep(1);
    left_motor.stop();
    left_motor.move(BACKWARD, 50);
    sleep(1);
    left_motor.stop();
    cout << "Finished first sequnce." << endl;

    right_motor.move(BACKWARD, 50);
    sleep(1);
    right_motor.stop();
    right_motor.move(FORWARD, 50);
    sleep(1);
    right_motor.stop();
    right_motor.move(BACKWARD, 50);
    sleep(1);
    right_motor.stop();

    right_motor.move(BACKWARD, 70);
    left_motor.move(BACKWARD, 70);
    sleep(1);
    right_motor.stop();
    left_motor.stop();
    right_motor.move(FORWARD, 40);
    left_motor.move(FORWARD, 40);
    sleep(1);
    right_motor.stop();
    left_motor.stop();
}

