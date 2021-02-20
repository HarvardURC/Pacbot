#include "sensors.hpp"
#include "../pac_pins.hpp"
#include "unistd.h"
extern "C" {
	#include "wiringPi.h"
}

Sensors::Sensors(){
	wiringPiSetup();
	sleep(0.5);
	int all_pins[4] = {pacBot_pins["tof_front"], pacBot_pins["tof_left"], pacBot_pins["tof_right"], pacBot_pins["tof_rear"]};

	for (int i = 0; i < 4; i++){
		pinMode(all_pins[i], OUTPUT);
		digitalWrite(all_pins[i], LOW);
		sleep(0.5);
	}
	this->front = new TofSensor(pacBot_pins["tof_front"], "front", 0x30);
	this->left = new TofSensor(pacBot_pins["tof_left"], "left", 0x31);
	this->right = new TofSensor(pacBot_pins["tof_right"], "right", 0x32);
	this->rear = new TofSensor(pacBot_pins["tof_rear"], "rear", 0x33);

}
