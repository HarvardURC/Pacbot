#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
//#include "vl6180_pi.h"
#include "movement.h"
#include "state.h"
#include "network.h"

#define RIGHT_MAX 99;
#define LEFT_MAX 100;

//vl6180 handle0;
//vl6180 handle1;
//vl6180 handle2;

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
    return; /*
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
	return; */
}

void setupMovement() {
    /*
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
    */
    return;
};

void all_init() {	
    
    setupMovement();
    /*
	softPwmCreate(pwmPinL, 0, 100);
	softPwmCreate(pwmPinR, 0, 100);
    */
	//while(1){
	//	go_straight();
		//turn_left();
	//}

}

void turn_right() {
    /*
	while (left_count < 123){
		digitalWrite(polarPinL, LOW);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, HIGH);
		softPwmWrite(pwmPinR, 50);
	}
	
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
    */
    return;
}

void turn_left() {
    /*
	left_count = 0;
	while (left_count < 115){
		digitalWrite(polarPinL, HIGH);
		softPwmWrite(pwmPinL, 50);
		digitalWrite(polarPinR, LOW);
		softPwmWrite(pwmPinR, 50);
	}

	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
    */
    return;
}

void turn_around(){
	turn_left();
	turn_left();
}

void correct_rot() {
    /*
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
    */
    return;
}

static int same_square(cell_pos a, cell_pos b) {
    if (a.cp_x == b.cp_x && a.cp_y == b.cp_y) {
        return 1;
    }
    return 0;
}

void go_straight() {
     /*
    int left;
    int right;
    int front;
    int right_init;
    int new_right;
    int left_init;
    int new_left;

	cell_pos pacbot_current;
	pollState();
	cell_pos pacbot_init = getPacbot();

	digitalWrite(polarPinL, LOW);
	digitalWrite(polarPinR, LOW);
	while(get_distance(handle0, 0x2a) > 31 &&
            same_square(pacbot_init, getPacbot())){
		
		left = get_distance(handle0, 0x2b);
		right = get_distance(handle0, 0x2c);
		if (right > left && right < 100){
			//printf("turn right\n");
			softPwmWrite(pwmPinL,50);
			if (left > 30)
				softPwmWrite(pwmPinR, 44 + 6*left/right);
			else
				softPwmWrite(pwmPinR, 40 + 10*left/right);
		}
		else if (left > right && left < 100){
			//printf("turn left\n");
			softPwmWrite(pwmPinR, 50);
			if (right > 30)
				softPwmWrite(pwmPinL, 44 + 6*right/left);
			else
				softPwmWrite(pwmPinL, 40 + 10*right/left);
		}
		else if (left > 100 && right < 100){
			//printf("left gap\n");
			right_init = right;
			while (get_distance(handle0, 0x2b) > 100 &&
                    get_distance(handle0, 0x2a) > 40 &&
                    same_square(pacbot_init, getPacbot())){
				new_right = get_distance(handle0, 0x2c);
				if (new_right > right_init || new_right > 44){
					softPwmWrite(pwmPinL, 50);
					softPwmWrite(pwmPinR, 49);
				}
				else {
					if (new_right < 30)
						softPwmWrite(pwmPinL, 48);
					else
						softPwmWrite(pwmPinL, 49);
					softPwmWrite(pwmPinR, 50);
				}
			}
		}
		else if (right > 100 && left < 100){
			left_init = left;
			while (get_distance(handle0, 0x2c) > 100 &&
                    get_distance(handle0, 0x2a) > 40 &&
                    same_square(pacbot_init, getPacbot())){
				new_left = get_distance(handle0, 0x2b);
				if (new_left > left_init || new_left > 44){
					softPwmWrite(pwmPinR, 50);
					softPwmWrite(pwmPinL, 49);
				}
				else {
					softPwmWrite(pwmPinL, 50);
					if (new_left < 30)
						softPwmWrite(pwmPinR, 48);
					else
						softPwmWrite(pwmPinR, 49);
				}
			}
		}
		else{
			softPwmWrite(pwmPinL, 49);
			softPwmWrite(pwmPinR, 50);
		}
	}

	forward_half();
	softPwmWrite(pwmPinL, 0);
	softPwmWrite(pwmPinR, 0);
    */
    return;
}

void forward_half(){
    /*
	left_count = 0;
	digitalWrite(polarPinL, LOW);
	digitalWrite(polarPinR, LOW);
	while (left_count < 60){
		softPwmWrite(pwmPinL, 50);
		softPwmWrite(pwmPinR, 50);
	}
	digitalWrite(pwmPinL, 0);
	digitalWrite(pwmPinR, 0);
    */
    return;
}

void left_add_count(){
	left_count += 1;
}
