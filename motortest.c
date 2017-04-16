#include <stdio.h>
#include <wiringPi.h>

// Pin number declarations
const int pwmPinL = 26;
const int polarPinL = 16;
const int pwmPinR = 13;
const int polarPinR = 6;

int main(void)
{
	wiringPiSetupGpio(); // Initializes wiringPi using the Broadcom GPIO pin numbers

	// left motor
	pinMode(pwmPinL, PWM_OUTPUT);
	pinMode(polarPinL, OUTPUT);
	// right motor
	pinMode(pwmPinR, PWM_OUTPUT);
	pinMode(polarPinR, OUTPUT);

	printf("Motor pins set! Press CTRL+C to exit!\n");
}
