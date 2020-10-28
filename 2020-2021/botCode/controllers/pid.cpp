#include "pid.hpp"

PID::PID(double kp, double ki, double kpredict, int d_smoother) {
    // kpredict = kd/kp, units = seconds
    this->errors = Deque<PID::ErrorLog>(d_smoother);
    set_kp(kp);
    set_ki(ki);
    set_kpredict(kpredict);
}

void PID::add_error(double error) {
    this->errors.add(PID::ErrorLog(error, time(NULL)));
    double de_dt = 0;
    add_error_w_deriv(error, de_dt);
}

void PID::add_error_w_deriv(double error, double de_dt) {
    this->output = this->kp * error + this->kd * de_dt + this->ki * ki;
}
double PID::get_output() { return output; }

double PID::get_kp() { return kp; }
double PID::get_ki() { return ki; }
double PID::get_kd() { return kd; }
double PID::get_prediction() { return kd / kp; }
int PID::get_smoother() { return this->errors.get_max_size(); }

void PID::set_kp(double kp) { this->kp = kp; }
void PID::set_ki(double ki) { this->ki = ki; }
void PID::set_kd(double kd) { this->kd = kd; }
void PID::set_kpredict(double kpredict) { this->kd = kpredict * this->kp; }