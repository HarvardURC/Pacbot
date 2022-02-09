# Harvard PacBot Design Overview 2018-19
(PCB design files and schematic can be found in public PacBot Design Folder)

## Electrical Components
-1 Raspberry Pi Zero W

-1 Teensy 3.5

-1 PCB

-1 IMU

-Assorted capacitors, resistors, wires

-4 IR Sensors

-2 Magnetic encoder pairs

-2 Motors

-1 Motor Driver

-Li-Po Battery

(specific links to components can be found at https://docs.google.com/spreadsheets/d/1ZO9OBoGcNkOdx6GaBkAFo6AWodeVCOaCXKic-0er2z0/edit?usp=sharing)

## Mechanical Components
-Wheels/Ball Casters

-3D Printed Battery Clip

## Code
All code can be found in the accompanying folders in this repo. We recommend looking at code from 2018-2019 because this year's code will be undergoing maintenance between now and the competition.

## Broad Overview
As the core processors for the bot, a Raspberry Pi Zero W and Teensy 3.5 were used. Nearly all of our high level and low level code ran off of our Raspberry Pi Zero W; the teensy was mainly used to interface with the encoders and other sensors. The entire bot was centered around the PCB. The motors directly attached to the PCB using small brackets, and all of the electrical components were soldered on in some manner. Although the schematic of the electrical components and the PCB design (which are in this folder) give an idea of the set up of our bot, we unfortunately do not have a SolidWorks design of our 2018-19 bot. A few photos of the 2018-19 bot in this folder help give a picture of the overall design.
