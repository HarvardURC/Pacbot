class TofSensor {
  public:
    TofSensor(int pin, int address);
    void set_address(int address);
    double get_distance();
};