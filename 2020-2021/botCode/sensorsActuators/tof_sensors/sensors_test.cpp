#include "sensors.hpp"
#include <iostream>
#include <unistd.h>

using namespace std;

int main(){
	Sensors mySensors = Sensors();
	
	while (1){
		cout << "Front: " << mySensors.front->distance() << endl;
		cout << "Rear: " << mySensors.rear->distance() << endl;
		cout << "Right: " << mySensors.right->distance() << endl;
		cout << "Left: " << mySensors.left->distance() << endl;
		sleep(1.0);
	}
}
