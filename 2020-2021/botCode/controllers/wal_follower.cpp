#include "../sensorsActuators/motors.hpp"
#include "../sensorsActuators/sensors.hpp"
#include "wall_follower.hpp"

wall_follower::wall_follower(double dist, bool follow_right) {
    this->pid = PID(wall_follower::kP, wall_follower::kI, wall_follower::kD);
    this->follow_right = follow_right;
}
void update() {
    TofSensor *sensor = this->follow_right ? right : left;
    double error = sensor->distance() - dist;
    int speed = 30;
    int output = this->pid.output();
    this->pid.update(error);
    this->left_motor->move(MotorDirection::FORWARD, speed + output);
    this->right_motor->move(MotorDirection::FORWARD, speed - output);
}
PID get_pid() { return this->pid; }