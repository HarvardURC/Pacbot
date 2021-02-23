#include "../sensors.hpp"
#include <iostream>
#include "wiringPi.h"
#include <thread>

using namespace std;

int main(){
	// WiringPi setup must be called before library is used
	wiringPiSetup();

	Sensors mySensors = Sensors();
	while (1){
		cout << "Front: " << mySensors.front->distance() << endl;
		cout << "Rear: " << mySensors.rear->distance() << endl;
		cout << "Right: " << mySensors.right->distance() << endl;
		cout << "Left: " << mySensors.left->distance() << endl;
		this_thread::sleep_for(1000ms);
	}
}
