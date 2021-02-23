#ifndef SENSORS_H
#define SENSORS_H

#include "./sa_interface/tofsensor.hpp"

/* PacBot specific sensors */
class Sensors{
	public:
		Sensors();
		TofSensor* front;
		TofSensor* rear;
		TofSensor* left;
		TofSensor* right;

};

#endif
