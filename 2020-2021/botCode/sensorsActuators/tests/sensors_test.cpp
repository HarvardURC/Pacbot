#include "../sensors.hpp"
#include <iostream>
#include "wiringPi.h"
#include <thread>

using namespace std;

int main(){
	// WiringPi setup must be called before library is used
	wiringPiSetup();
	initialize_sensors();

	while (1){
		cout << "Front: " << front_tof->distance() << endl;
		cout << "Rear: " << rear_tof->distance() << endl;
		cout << "Right: " << right_tof->distance() << endl;
		cout << "Left: " << left_tof->distance() << endl;
		this_thread::sleep_for(1000ms);
	}
}
