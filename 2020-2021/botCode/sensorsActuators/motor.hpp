enum MotorDirection { Forward, Backwards, Stop };

class Motor {
  public:
    Motor(int power_pin, int direction_pin);
    void set_power(double power, MotorDirection direction);
};