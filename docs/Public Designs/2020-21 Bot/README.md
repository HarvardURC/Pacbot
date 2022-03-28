# Harvard PacBot Design Overview 2020-21
PCB design files and images of the bot can be found in this directory.

## Electrical Components
-1 Raspberry Pi Zero W

-1 Teensy 3.5

-1 PCB

-1 IMU (not in images)

-4 IR Sensors

-2 Magnetic encoder pairs

-2 Motors

-1 Motor Driver

-Li-Po Battery

-1 voltage regulator

(specific links to components can be found at https://docs.google.com/spreadsheets/d/1ZO9OBoGcNkOdx6GaBkAFo6AWodeVCOaCXKic-0er2z0/edit?usp=sharing)

## Mechanical Components
-Wheels/Ball Casters

## Broad Overview
### Sensors

IR sensors are used for detecting whether we are near walls. These are placed on the sides and the front/back of the bot (see photos). Past robots used PID control on these sensors to follow the walls.

Magnetic encoders are attached to the motors to track the amount of distance we travel.

An IMU was intended to be used for general navigation of the robot (to ensure we don't hit walls and turn accurately - other uses are possible). It's not present in the photos.

### Processors

A Raspberry Pi Zero W is used to interface with the motors (through the motor driver) and the IR sensors. It also connects to our local wifi network in order to receive instructions from a computer regarding where the bot should travel (the high level code would run on a remote computer and send commands to the PacBot).

Because of the encoder's output requirements, a Teensy is used to receive the encoder readings. The Teensy is also connected to the IMU. The Teensy communicates these sensor readings to the Raspberry Pi via serial communication.

### Motors

Two medium power, 6V, brushed DC gear motors are used on our bot (see https://www.pololu.com/product/2381). A motor driver is necessary to communicate with the motors from the Raspberry Pi. The encoders are attached to the motors.

### PCB

All of our electrical components are connected via a Printed Circuit Board. This is the main "structure" of our bot; all components are soldered onto this. The KiCad files for the PCB can be found in this directory.

### Code

All of the code for our bot (high level and low level) can be found in the *src/botCode* directory of this GitHub repo.
