# Overview of Low Level Code

## teensy_code

This contains code for the teensy. The final code running on the teensy was `teensy_code/sensors/sensors.ino`. Make sure to fulfill the requirements in the requirements.txt file if loading to the teensy. Also, if you're loading this to the teensy on the 2021-2022 bot, you'll need to modify your Teensy Wire library such that Wire1 is defined. Specifically, uncomment `#define WIRE_IMPLEMENT_WIRE1` in WireKinetis.h.

I recommend using TeensyDuino with the teensy. I think these instructions are alright for Teensy: https://www.pjrc.com/teensy/td_usage.html. With the Arduino IDE, make sure you have the correct Board and Port selected under Tools. Also, to load a sketch onto the Teensy, you only need to press the Compile button and the button on the Teensy. DON'T press the Arduino IDE Upload button.

## motors.py

motors.py controls the motors. It uses PIDs of the IMU to turn to the direction we want to go and go straight. directionLowLevelModule.py tells this what direction to take our robot.

## sensors.py and tofSensor.py

These are for controlling our IR sensors.

## teensySensors.py

This is for reading from the serial port to get the Encoder and IMU measurements from the Teensy.