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

void main() {
	all_init();
	while (1) {
	    /*while(getGameStatus() == P_STOPPED) {
	        pollState();
	    }*/
	    while (pollState() = 0){
	    	digitalWrite(pwmPinL, 0);
	    	digitalWrite(pwmPinR, 0);
	    }
	    while (pollState() == 1){
	    	digitalWrite(polarPinL, LOW);
	    	digitalWrite(polarPinR, LOW);
	    	softPwmWrite(pwmPinL, 50);
	    	softPwmWrite(pwmPinR, 50);
	    }
	    while (pollState() == 2){
	    	digitalWrite(polarPinL, LOw);
	    	digitalWrite(polarPinR, HIGH);
	    	softPwmWrite(pwmPinL, 25);
	    	softPwmWrite(pwmPinR, 25);
	    }
	    while (pollState() == 3){
	    	digitalWrite(polarPinL, HIGH);
	    	digitalWrite(polarPinR, HIGH);
	    	softPwmWrite(pwmPinL, 50);
	    	softPwmWrite(pwmPinR, 50);
	    }
	}
}