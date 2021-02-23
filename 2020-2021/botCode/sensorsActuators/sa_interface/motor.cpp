#include "motor.hpp"
#include <softPwm.h>
#include <wiringPi.h>

Motor::Motor(int power_pin, int direction_pin) {
    this->power_pin = power_pin;
    this->direction_pin = direction_pin;
    printf("variables set\n");
    softPwmCreate(this->power_pin, 0, 100);
    printf("pwm create\n");
    pinMode(this->direction_pin, OUTPUT);
    printf("pin mode\n");
}

void Motor::move(MotorDirection direction, int speed) {
    if (direction == STOP) {
        softPwmWrite(this->power_pin, 0);
    } else {
        digitalWrite(this->direction_pin, direction);
        softPwmWrite(this->power_pin, speed);
    }
}

void Motor::stop() { softPwmWrite(this->power_pin, 0); }
