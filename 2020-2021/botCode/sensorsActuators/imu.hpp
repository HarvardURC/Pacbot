class IMU {
  public:
    IMU(int pin, int address);
    double get_yaw();
    double get_pitch();
    double get_heading();
};