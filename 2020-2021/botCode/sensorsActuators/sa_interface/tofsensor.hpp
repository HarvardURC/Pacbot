#ifndef TOFSENSOR_H
#define TOFSENSOR_H

#include <vl6180_pi/vl6180_pi.h>
#include <string>

using namespace std;

/* Time of Flight Sensors - Specifically vl6180_x tof sensors*/
class TofSensor{
	public:
		TofSensor(int pin, string name, int address);
		int distance();
		int pin;
		string name;
		int address;
	private:
		vl6180 handle;
};
#endif
