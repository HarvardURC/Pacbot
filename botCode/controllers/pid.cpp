#ifndef PID_H
#define PID_H

#include "pid.hpp"

PID::PID(double kp, double ki, double kpredict, int d_smoother) {
    // kpredict = kd/kp, units = seconds
    this->errors.resize(d_smoother);
    set_kp(kp);
    set_ki(ki);
    set_kpredict(kpredict);
}

void PID::add_error(double error) {
    time_t tm = time(NULL);
    double de = error - this->errors.back().error;
    double dt = difftime(tm, this->errors.back().time);
    double de_dt = dt == 0 ? 0 : de / dt;
    this->integral += 0.5 * dt * (error + this->errors.back().error);
    this->output =
        this->kp * error + this->kd * de_dt + this->ki * this->integral;
    this->errors.push_front(PID::ErrorLog(error, tm));
}
double PID::get_output() { return output; }

double PID::get_kp() { return kp; }
double PID::get_ki() { return ki; }
double PID::get_kd() { return kd; }
double PID::get_prediction() { return kp == 0. ? 0. : kd / kp; }
int PID::get_smoother() { return this->errors.max_size(); }

void PID::set_kp(double kp) { this->kp = kp; }
void PID::set_ki(double ki) { this->ki = ki; }
void PID::set_kd(double kd) { this->kd = kd; }
void PID::set_kpredict(double kpredict) { this->kd = kpredict * this->kp; }

#endif