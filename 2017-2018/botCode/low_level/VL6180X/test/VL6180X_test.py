#!/usr/bin/python

""" ST VL6180X ToF range finder program
 - power explorer board with 3.3 V
 - explorer board includes pull-ups on i2c """

import sys
from ST_VL6180X import VL6180X
from time import sleep
import RPi.GPIO as GPIO  # Import GPIO functions

"""-- Setup --"""
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

# setup ToF ranging/ALS sensor
tof_address = 0x29
tof_sensor = VL6180X(address=tof_address, debug=debug)
tof_sensor.get_identification()
if tof_sensor.idModel != 0xB4:
    print"Not a valid sensor id: %X" % tof_sensor.idModel
else:
    print"Sensor model: %X" % tof_sensor.idModel
    print"Sensor model rev.: %d.%d" % \
         (tof_sensor.idModelRevMajor, tof_sensor.idModelRevMinor)
    print"Sensor module rev.: %d.%d" % \
         (tof_sensor.idModuleRevMajor, tof_sensor.idModuleRevMinor)
    print"Sensor date/time: %X/%X" % (tof_sensor.idDate, tof_sensor.idTime)
tof_sensor.default_settings()

# Set output pin numbers for LEDS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use GPIO numbering scheme (not pin numbers)
LED = [17, 27]          # List of GPIOs to use for LED output
for i in range(len(LED)):
    GPIO.setup(LED[i], GPIO.OUT)  # Set all as output
    print("GPIO_%d is output" % LED[i])
    GPIO.output(LED[i], 0)  # Turn all LEDs off

sleep(1)

"""-- MAIN LOOP --"""
while True:
    print "Measured distance is : %d mm" % tof_sensor.get_distance()
    print "Measured light level is : %d lux" % tof_sensor.get_ambient_light(20)
    sleep(1)
