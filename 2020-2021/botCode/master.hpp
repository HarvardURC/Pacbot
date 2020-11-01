// This file will run on loop and control the robot
#include "utils/conversions.hpp"
class Master {
  private:
    static void on_init();
    static void on_periodic();
    static void loop();

  public:
    static double TICK_LENGTH = ;
    static void start();
};