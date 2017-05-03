#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include "vl6180_pi.h"
#include "movement.h"
#include "state.h"
#include "network.h"

#define RIGHT_MAX 99;
#define LEFT_MAX 100;

vl6180 handle0;

int distance0;
int distance1;
int distance2;

int left_count = 0;
int right_count = 0;


int left;
int right;
int front;
int right_init;
int new_right;
int left_init;
int new_left;
int off;

const int max_thresh = 100;
const int front_thresh = 31;
const int min_thresh = 30;

// Pin number declarations for motors and encoders
const int pwmPinL = 26;
const int polarPinL = 19;
const int pwmPinR = 13;
const int polarPinR = 6;
const int EncR = 18;
const int EncL = 18;

int counter;
int error = 0;

// interrupt syntax for wiringPi library
int wiringPiISR (int pin, int edgeType,  void (*function)(void)) ;

static int MAX(int a, int b){
	if (a > b)
		return a;
	else
		return b;
}

static int MIN(int a, int b){
	if (a > b)
		return b;
	else
		return a;
}

void initialise_irs(){
    digitalWrite(20, LOW);
	digitalWrite(22, LOW);
	digitalWrite(27, LOW);
	//handle0 = vl6180_initialise(1, 0);
	// Write all reset pins high
	digitalWrite(20, HIGH);
	digitalWrite(22, HIGH);
	digitalWrite(27, HIGH);

	// Initialise all with 0x029 address
	handle0 = vl6180_initialise(1, 0);

	// Only enable the front IR reset pin
	digitalWrite(20, LOW);
	digitalWrite(22, LOW);
	// change it's I2C slave address
	change_address(handle0, 0x2a);

	// enable left IR pin and initialise
	/*
	Note: don't have to disable front pin because its address is changed
	and we are only communicating with devices with addresses 0x29
	*/
	digitalWrite(20, HIGH);
	handle0 = vl6180_initialise(1, 0);
	//change it's I2C slave address
	change_address(handle0, 0x2b);
	//Same for right IR sensor;
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
	initialise_irs();
	delay(500);
    
};

void all_init() {	
    
    setupMovement();
	softPwmCreate(pwmPinL, 0, 100);
	softPwmCreate(pwmPinR, 0, 100);
	counter = 0;
}

// Turn right function	
void turn_right(){
	// initialize counter
	left_count = 0;

	// Until it reaches a value determined through experimentation
	while (left_count < 103){

		// Set proper polarity (left motor forward, right reverse)
		// Power motors
		digitalWrite(polarPinL, LOW);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, HIGH);
		softPwmWrite(pwmPinR, 50);
	}
	
	// cut power to motors;
	digitalWrite(pwmPinL, 0);
	digitalWrite(pwmPinR, 0);
	error = 0;
	return;
}

// Same idea as above
void turn_left(void){
	left_count = 0;
	while (left_count < 133){
		digitalWrite(polarPinL, HIGH);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, LOW);
		softPwmWrite(pwmPinR, 50);
	}

	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
	error = 0;
	return; 
}

void turn_around(){
	turn_left();
	turn_left();
}

// Correct for misalignment, didn't end up using this function
void correct_rot(){
	// check if the front of the bot is too close to left wall
	if(get_ir_distance (handle0, 0x2b) < 42){
		digitalWrite(polarPinL, HIGH);
		digitalWrite(polarPinR, LOW);
		// turn until not too close to wall
		while(get_ir_distance (handle0, 0x2b) < 42){
			softPwmWrite(pwmPinL, 20);
			softPwmWrite(pwmPinR, 20);
		}
	}

	// otherwise it's too close to right wall
	else{
		digitalWrite(polarPinL, LOW);
		digitalWrite(polarPinR, HIGH);
		while(get_ir_distance (handle0, 0x2b) > 42){
			softPwmWrite(pwmPinL, 20);
			softPwmWrite(pwmPinR, 20);
		}
	}

	// cut power to motors
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
	return;
}

static int same_square(cell_pos a) {
    pollState();
    cell_pos b = getPacbot();
    if (a.cp_x == b.cp_x && a.cp_y == b.cp_y) {
        return 1;
    }
    return 0;
}

// for when you need to go straight
void go_straight(){

	// create I variable of PID
    cell_pos pacbot_init = getPacbot(); 
	// set motor polarities
	digitalWrite(polarPinL, LOW);
	digitalWrite(polarPinR, LOW);
	// as long as there's not a wall in front
	while(same_square(pacbot_init)){
		// Check distance from neighboring walls
		left = get_ir_distance (handle0, 0x2b);
		right = get_ir_distance (handle0, 0x2c);
		
		// If closer to left wall and not at a gap (aka walls on both sides)
		if (right > left && right < 100){
			off = (right - left)/2;
			softPwmWrite(pwmPinL,49);
			error += off;
			error = MIN(33, error);
			error = MAX(-33, error);
			softPwmWrite(pwmPinR, MAX(47, MIN(50, 50 - 0.1 * off - 0.03*error)));
		}
		else if (left > right && left < 100){
			off = (right - left)/2;
			error += off;
			error = MIN(33, error);
			error = MAX(-33, error);
			softPwmWrite(pwmPinR, 50);
			softPwmWrite(pwmPinL, MAX(47, MIN(50 + 0.1 * off + 0.03*error,50)));
		}
		else if (left > 100 && right < 75){
			right_init = right;
			while (get_ir_distance (handle0, 0x2b) > 100 &&
                    same_square(pacbot_init)){
				new_right = get_ir_distance (handle0, 0x2c);
				off = new_right - 42;
				if (abs(off) < 5)
					error = 0;
				error += off;
				error = MIN(33, error);
				error = MAX(-33, error);
				if (off > 0){
					softPwmWrite(pwmPinL, 49);
					softPwmWrite(pwmPinR, MAX(47, MIN(50 - 0.1 * off - 0.03*error, 50)));
				}
				else {
					softPwmWrite(pwmPinL, MAX(47, MIN(50 + 0.1*off + 0.03*error, 50))); 
					softPwmWrite(pwmPinR, 50);
				}
			}
		}
		else if (right > 100 && left < 75){
			left_init = left;
			while (get_ir_distance (handle0, 0x2c) > 100 &&
                    same_square(pacbot_init)){
				new_left = get_ir_distance (handle0, 0x2b);
				off = 42 - new_left;
				if (abs(off) < 5)
					error = 0;
				error += off;
				error = MIN(33, error);
				error = MAX(-33, error);
				if (off < 0){
					softPwmWrite(pwmPinR, 50);
					softPwmWrite(pwmPinL, MAX(47, MIN(50, 50 + 0.1*off + 0.03*error)));
				}
				else {
					softPwmWrite(pwmPinL, 49);
					softPwmWrite(pwmPinR, MAX(47, MIN(50, 50 - 0.1*off - 0.03*error)));
				}
			}
		}
		else {
			if (off < 0){
				softPwmWrite(pwmPinL, MAX(48, MIN(50, 50 + 0.03 * off)));
				softPwmWrite(pwmPinR, 50);
			}
			else {
				softPwmWrite(pwmPinR, MAX(48, MIN(50, 50 - 0.05 * off)));
				softPwmWrite(pwmPinL, 49);
			}
		}
		if (abs(left - right) < 5 && left < 100)
			error = 0;
	}
	left_count = 0;
    while(left_count < 60){
		// Check distance from neighboring walls
		left = get_ir_distance (handle0, 0x2b);
		right = get_ir_distance (handle0, 0x2c);
		
		// If closer to left wall and not at a gap (aka walls on both sides)
		if (right > left && right < 100){
			off = (right - left)/2;
			softPwmWrite(pwmPinL,49);
			error += off;
			error = MIN(33, error);
			error = MAX(-33, error);
			softPwmWrite(pwmPinR, MAX(47, MIN(50, 50 - 0.1 * off - 0.03*error)));
		}
		else if (left > right && left < 100){
			off = (right - left)/2;
			error += off;
			error = MIN(33, error);
			error = MAX(-33, error);
			softPwmWrite(pwmPinR, 50);
			softPwmWrite(pwmPinL, MAX(47, MIN(50 + 0.1 * off + 0.03*error,50)));
		}
		else if (left > 100 && right < 75){
			right_init = right;
			while (get_ir_distance (handle0, 0x2b) > 100 &&
                    left_count < 60){
				new_right = get_ir_distance (handle0, 0x2c);
				off = new_right - 42;
				if (abs(off) < 5)
					error = 0;
				error += off;
				error = MIN(33, error);
				error = MAX(-33, error);
				if (off > 0){
					softPwmWrite(pwmPinL, 49);
					softPwmWrite(pwmPinR, MAX(47, MIN(50 - 0.1 * off - 0.03*error, 50)));
				}
				else {
					softPwmWrite(pwmPinL, MAX(47, MIN(50 + 0.1*off + 0.03*error, 50))); 
					softPwmWrite(pwmPinR, 50);
				}
			}
		}
		else if (right > 100 && left < 75){
			left_init = left;
			while (get_ir_distance (handle0, 0x2c) > 100 &&
                    left_count < 60){
				new_left = get_ir_distance (handle0, 0x2b);
				off = 42 - new_left;
				if (abs(off) < 5)
					error = 0;
				error += off;
				error = MIN(33, error);
				error = MAX(-33, error);
				if (off < 0){
					softPwmWrite(pwmPinR, 50);
					softPwmWrite(pwmPinL, MAX(47, MIN(50, 50 + 0.1*off + 0.03*error)));
				}
				else {
					softPwmWrite(pwmPinL, 49);
					softPwmWrite(pwmPinR, MAX(47, MIN(50, 50 - 0.1*off - 0.03*error)));
				}
			}
		}
		else {
			if (off < 0){
				softPwmWrite(pwmPinL, MAX(48, MIN(50, 50 + 0.03 * off)));
				softPwmWrite(pwmPinR, 50);
			}
			else {
				softPwmWrite(pwmPinR, MAX(48, MIN(50, 50 - 0.05 * off)));
				softPwmWrite(pwmPinL, 49);
			}
		}
		if (abs(left - right) < 5 && left < 100)
			error = 0;
	}
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
	return;
}


// When entering a new grid unit, want to go to center; aka half the grid unit
void forward_half(){
	// initialize the counter to 0
	left_count = 0;

	// set both motors in proper direction
	digitalWrite(polarPinL, LOW);
	digitalWrite(polarPinR, LOW);

	// until you've gone 60 clicks, go forward
	while (left_count < 60){
		if (off < 0){
				softPwmWrite(pwmPinL, MAX(48, MIN(50, 50 + 0.03 * off)));
				softPwmWrite(pwmPinR, 50);
			}
		else {
				softPwmWrite(pwmPinR, MAX(48, MIN(50, 50 - 0.05 * off)));
				softPwmWrite(pwmPinL, 49);
		}
	}

	// cut power to motors;
	digitalWrite(pwmPinL, 0);
	digitalWrite(pwmPinR, 0);
}

void left_add_count(){
	left_count += 1;
}
