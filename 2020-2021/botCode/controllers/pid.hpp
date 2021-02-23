#ifndef PID_H
#define PID_H

#include "../dataTypes/deque.cpp"
#include <chrono>
#include <time.h>

typedef std::chrono::high_resolution_clock Clock;

class PID {
  private:
    struct ErrorLog {
        double error;
        Clock::time_point time;
        ErrorLog(double error, Clock::time_point time) {
            this->error = error;
            this->time = time;
        }
        ErrorLog() {
            this->error = 0;
            this->time = Clock::now();
        }
    };
    double kp, ki, kd, output, integral;
    Deque<ErrorLog> errors;

  public:
    // Number of errors to look back
    static const int DEFAULT_D_SMOOTHER = 5;
    PID();
    PID(double kp, double ki, double kd, int d_smoother = DEFAULT_D_SMOOTHER);
    static PID PID_predict(double kp, double ki, double kpredict,
                           int d_smoother = DEFAULT_D_SMOOTHER);

    void add_error(double error);
    double get_output();

    double get_kp();
    double get_ki();
    double get_kd();
    double get_prediction();
    int get_smoother();

    void set_kp(double kp);
    void set_ki(double ki);
    void set_kd(double kd);
    void set_kpredict(double kpredict);
};

#endif