#include <time.h>

#include <deque>

class PID {
  private:
    struct ErrorLog {
        double error;
        time_t time;
        ErrorLog(double error, time_t time) {
            this->error = error;
            this->time = time;
        }
        ErrorLog() {
            this->error = 0;
            this->time = 0;
        }
    };
    double kp, ki, kd, output, integral;
    std::deque<ErrorLog> errors;

  public:
    // Number of errors to look back
    static const int DEFAULT_D_SMOOTHER = 5;
    PID(double kp, double ki, double kpredict,
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