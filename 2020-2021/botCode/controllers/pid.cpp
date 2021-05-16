#include "pid.hpp"
#include "../utils/conversions.hpp"

typedef std::chrono::milliseconds milliseconds;

// What is k_predict? Here's the idea:
// If you have some kp, and some kd, it's not immediatly obvious what the kd
// means? Well, here's my intuition.
// output = kp*e + kd*(de/dt), that we know.
// If we factor out the kp constant (this will make sense in a second) we get:
// output = kp(e + kd/kp * (de/dt))
// Now we can say e' = e + kd/kp * (de/dt)
// So our output = kp*e', but that just looks like a p controller!
// And e' is simply a linear approximation of e in kd/kp seconds.
// So, the (kd/kp) constant becoems a more natural constant to think about, it's
//     how far forward you want to predict!
// We call this constant k_predict

PID::PID(double kp, double ki, double kd, int d_smoother) {
    // kpredict = kd/kp, units = seconds
    this->errors = Deque<ErrorLog>(d_smoother);
    set_kp(kp);
    set_ki(ki);
    set_kd(kd);
}
PID::PID() {
    this->errors = Deque<ErrorLog>(1);
    set_kp(0);
    set_ki(0);
    set_kd(0);
}

PID PID::PID_predict(double kp, double ki, double kpredict, int d_smoother) {
    // kpredict = kd/kp, units = seconds
    PID pid = PID(kp, ki, 0, d_smoother);
    pid.set_kpredict(kpredict);
    return pid;
}

void PID::add_error(double error) {
    Clock::time_point tm = Clock::now();
    this->errors.add(PID::ErrorLog(error, tm));
    printf("length: %d\n", this->errors.length());
    double de = error - this->errors.last().error;
    printf("got last\n");
    double dt =
        millis_to_secs(std::chrono::duration_cast<std::chrono::milliseconds>(
                           tm - this->errors.last().time)
                           .count());
    double de_dt = dt == 0 ? 0 : de / dt;
    this->integral += 0.5 * dt * (error + this->errors.last().error);
    this->output =
        this->kp * error + this->kd * de_dt + this->ki * this->integral;
    printf("DT: %f, de: %f, kp: %f, kd: %f, output: %f\n", dt, de, this->kp,
           this->kd, this->output);
}
double PID::get_output() { return output; }

double PID::get_kp() { return kp; }
double PID::get_ki() { return ki; }
double PID::get_kd() { return kd; }
double PID::get_prediction() { return kp == 0. ? 0. : kd / kp; }
int PID::get_smoother() { return this->errors.get_max_size(); }

void PID::set_kp(double kp) { this->kp = kp; }
void PID::set_ki(double ki) { this->ki = ki; }
void PID::set_kd(double kd) { this->kd = kd; }
void PID::set_kpredict(double kpredict) { this->kd = kpredict * this->kp; }
