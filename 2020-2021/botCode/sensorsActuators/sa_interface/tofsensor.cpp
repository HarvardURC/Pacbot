#include "tofsensor.hpp"
#include <string>
#include <thread>
#include <unistd.h>
#include <vl6180_pi/vl6180_pi.h>
#include <wiringPi.h>

TofSensor::TofSensor(int pin, string name, int address) {
    this->pin = pin;
    this->name = name;
    this->address = address;

    // setting Input pin on sensor to PUD_UP activates the sensor
    pinMode(pin, INPUT);
    pullUpDnControl(pin, PUD_UP);
    std::this_thread::sleep_for(250ms);

    this->handle = vl6180_initialise_address(1, 0x29);
    vl6180_change_addr(this->handle, address);

    // after testing, it appears that it takes time for
    // sensor to actually take on the address - thus sleep this thread
    std::this_thread::sleep_for(5000ms);
}

// get measure time-of-flight distance
double TofSensor::distance() {
    return ((double)get_distance(this->handle)) / 1000.;
}
