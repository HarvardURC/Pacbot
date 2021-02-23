#include "../motors.hpp"
#include "../sa_interface/motor.hpp"
#include <iostream>
#include <unistd.h>

#include <wiringPi.h>

using namespace std;

int main(void){
    // Wiring pi needs to be setup at the start of the program!
    wiringPiSetup();
    
    Motors pac_motors = Motors();
    Motor *left_motor = pac_motors.left;
    Motor *right_motor = pac_motors.right;

    cout << "Motors Initialized." << endl;

    left_motor->move(BACKWARD, 50);
    sleep(1);
    left_motor->stop();
    left_motor->move(FORWARD, 50);
    sleep(1);
    left_motor->stop();
    left_motor->move(BACKWARD, 50);
    sleep(1);
    left_motor->stop();
    cout << "Finished first sequnce." << endl;

    right_motor->move(BACKWARD, 50);
    sleep(1);
    right_motor->stop();
    right_motor->move(FORWARD, 50);
    sleep(1);
    right_motor->stop();
    right_motor->move(BACKWARD, 50);
    sleep(1);
    right_motor->stop();

    right_motor->move(BACKWARD, 70);
    left_motor->move(BACKWARD, 70);
    sleep(1);
    right_motor->stop();
    left_motor->stop();
    right_motor->move(FORWARD, 40);
    left_motor->move(FORWARD, 40);
    sleep(1);
    right_motor->stop();
    left_motor->stop();
    cout << "Finished full sequence." << endl;
    sleep(1.5);
}

