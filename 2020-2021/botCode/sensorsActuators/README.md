## Sensors And Actuators

This folder contains files that have the abstract ability to directly talk to specific _kinds_ of sensors and actuators. However, this folder contains no references to physical "instances" of sensors and actuators. For instance, you might have a file that allows one to deals with motors, but there will be no reference to the specific motors on the chassis of the robot.

The library wiringPi.h is used to interface with the GPIO pins on the Raspberry PI. wiringPiSetup() must be called immediately when the programmer starts running to use this library.
