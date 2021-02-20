#include "motor.hpp"

extern "C" {
    #include <wiringPi.h>
    #include <softPwm.h>
}

Motor::Motor(int power_pin, int direction_pin){

    this->power_pin = power_pin;
    this->direction_pin = direction_pin;
    softPwmCreate(this->power_pin, 0, 100);
    pinMode(this->direction_pin, OUTPUT);
}

void Motor::move(MotorDirection direction, int speed){
    if (direction == STOP){
        softPwmWrite(this->power_pin, 0);
    } else {
        digitalWrite(this->direction_pin, direction);
        softPwmWrite(this->power_pin, speed);
    }
}

void Motor::stop(){
    softPwmWrite(this->power_pin, 0);
}

