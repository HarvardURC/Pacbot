#ifndef SENSORS_H
#define SENSORS_H

#include "tofsensor.hpp"

class Sensors{
	public:
		Sensors();
		TofSensor* front;
		TofSensor* rear;
		TofSensor* left;
		TofSensor* right;

};

#endif
