#ifndef MOTOR_H
#define MOTOR_H

enum MotorDirection{BACKWARD, FORWARD, STOP};

/* class for motors */
class Motor{
    public:
        Motor(int power_pin, int direction_pin);
        int power_pin;
        int direction_pin;
        void move(MotorDirection direction, int speed);
        void stop();

};

#endif

