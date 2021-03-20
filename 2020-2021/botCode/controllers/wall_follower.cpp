#include "wall_follower.hpp"
#include "../sensorsActuators/motors.hpp"
#include "../sensorsActuators/sensors.hpp"

wall_follower::wall_follower(double dist, bool follow_right) {
    this->pid = PID(0.3, 0., 0.);
    // PID(wall_follower::kP, wall_follower::kI, wall_follower::kD);
    this->dist = dist;
    this->follow_right = follow_right;
}
void wall_follower::update() {
    TofSensor *sensor =
        this->follow_right ? right_tof : left_tof;
    double error = sensor->distance() - this->dist;
    this->pid.add_error(error);
    int speed = 40;
    int output = this->pid.get_output();
    left_motor->move(MotorDirection::FORWARD, speed + output);
    right_motor->move(MotorDirection::FORWARD, speed - output);
}
PID wall_follower::get_pid() { return this->pid; }
