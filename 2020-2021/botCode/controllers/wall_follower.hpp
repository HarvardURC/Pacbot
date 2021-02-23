#ifndef WALL_FOLLOWER_H
#define WALL_FOLLOWER_H
#include "pid.hpp"

class wall_follower {
  private:
    PID pid;
    /*const static double kP = 0.3;
    const static double kI = 0.;
    const static double kD = 0.;*/
    bool follow_right;

  public:
    wall_follower(double dist, bool follow_right);
    void update();
    PID get_pid();
};

#endif