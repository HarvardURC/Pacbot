#include "vl6180_pi.h"
#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define RIGHT_MAX 99;
#define LEFT_MAX 100;

vl6180 handle0;
vl6180 handle1;
vl6180 handle2;

int left_count = 0;
int right_count = 0;
const int thresh = 100;

// Pin number declarations
const int pwmPinL = 26;
const int polarPinL = 19;
const int pwmPinR = 13;
const int polarPinR = 6;
const int EncR = 18;
const int EncL = 24;

void initialise_irs(){
	digitalWrite(20, HIGH);
	digitalWrite(22, HIGH);
	digitalWrite(27, HIGH);

	handle0 = vl6180_initialise(1, 0);

	digitalWrite(20, LOW);
	digitalWrite(22, LOW);
	digitalWrite(27, HIGH);
	change_address(handle0, 0x2a);

	digitalWrite(20, HIGH);
	handle0 = vl6180_initialise(1, 0);
	change_address(handle0, 0x2b);

	digitalWrite(22, HIGH);
	handle0 = vl6180_initialise(1, 0);
	change_address(handle0, 0x2c);
	return; 
}

void setupMovement() {
    wiringPiSetup();
	wiringPiSetupGpio();

	pinMode(20, OUTPUT);
	pinMode(22, OUTPUT);	
	pinMode(27, OUTPUT);

	pinMode(pwmPinL, OUTPUT);
	pinMode(pwmPinR, OUTPUT);
	pinMode(polarPinL, OUTPUT);
	pinMode(polarPinR, OUTPUT);

	pinMode(EncR, INPUT);
	pinMode(EncL, INPUT);

	wiringPiISR(EncL, INT_EDGE_RISING, *left_add_count);

	initialise_irs()
};

void all_init() {	
    
    setupMovement();

	softPwmCreate(pwmPinL, 0, 100);
	softPwmCreate(pwmPinR, 0, 100);

	//while(1){
		go_straight();
		//turn_left();
	//}

}

void turn_right() {
	while (left_count < 121){
		digitalWrite(polarPinL, LOW);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, HIGH);
		softPwmWrite(pwmPinR, 50);
	}
	
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
}

void turn_left() {
	left_count = 0;
	while (left_count < 121){
		digitalWrite(polarPinL, HIGH);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, LOW);
		softPwmWrite(pwmPinR, 50);
	}

	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
}

void correct_rot() {
	if(get_distance(handle0, 0x2b) < 42){
		digitalWrite(polarPinL, HIGH);
		digitalWrite(polarPinR, LOW);
		while(get_distance(handle0, 0x2b) < 42){
			softPwmWrite(pwmPinL, 20);
			softPwmWrite(pwmPinR, 20);
		}
	}
	else{
		digitalWrite(polarPinL, LOW);
		digitalWrite(polarPinR, HIGH);
		while(get_distance(handle0, 0x2b) > 42){
			softPwmWrite(pwmPinL, 20);
			softPwmWrite(pwmPinR, 20);
		}
	}

	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
	return 0;
}

void go_straight() {
    int left;
    int right;
    int front;
    int right_init;
    int new_right;
    int left_init;
    int new_left;

	digitalWrite(polarPinL, LOW);
	digitalWrite(polarPinR, LOW);
	while(get_distance(handle0, 0x2a) > 40){
		
		left = get_distance(handle0, 0x2b);
		right = get_distance(handle0, 0x2c);
		if (right > left && right < 100){
			//printf("turn right\n");
			softPwmWrite(pwmPinL,50);
			softPwmWrite(pwmPinR, 50*left/right);
		}
		else if (left > right && left < 100){
			//printf("turn left\n");
			softPwmWrite(pwmPinL, 50*right/left);
			softPwmWrite(pwmPinR, 50);
		}
		else if (left > 100){
			//printf("left gap\n");
			right_init = right;
			while (get_distance(handle0, 0x2b) > 100 && get_distance(handle0, 0x2a) > 40){
				new_right = get_distance(handle0, 0x2c);
				if (new_right > right_init){
					softPwmWrite(pwmPinL, 50);
					softPwmWrite(pwmPinR, right_init/new_right*50);
				}
				else {
					softPwmWrite(pwmPinL, right/right_init*50);
					softPwmWrite(pwmPinR, 50);
				}
			}
		}
		else if (right > 100){
			left_init = left;
			while (get_distance(handle0, 0x2c) > 100 && get_distance(handle0, 0x2a) > 40){
				new_left = get_distance(handle0, 0x2b);
				if (new_left > left_init){
					softPwmWrite(pwmPinR, 50);
					digitalWrite(polarPinR, LOW);
					softPwmWrite(pwmPinL, left_init/new_left*50);
					digitalWrite(polarPinL, HIGH);
				}
				else {
					softPwmWrite(pwmPinL, 50);
					digitalWrite(polarPinL, HIGH);
					softPwmWrite(pwmPinR, new_left/left_init*50);
					digitalWrite(polarPinR, LOW);
				}
			}
		}
	}
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
}

void left_add_count(){
	left_count += 1;
}
