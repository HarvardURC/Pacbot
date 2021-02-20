#include "tofsensor.hpp"
#include <vl6180_pi/vl6180_pi.h>
#include <string>
#include <unistd.h>

extern "C" {
	#include <wiringPi.h>
}
using namespace std;

TofSensor::TofSensor(int pin, string name, int address){
	this->pin = pin;
	this->name = name;
	this->address = address;
	pinMode(pin, INPUT);
	pullUpDnControl(pin, PUD_UP);
	sleep(0.25);
	this->handle = vl6180_initialise_address(1,0x29);
	vl6180_change_addr(this->handle, address);
	sleep(5.0);
}

int TofSensor::distance(){
	return get_distance(this->handle);
}
