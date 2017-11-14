import sys
import ST_VL6180X.ST_VL6180X
from time import sleep
from pins import *
from GPIOhelpers import *


# sensor_pins = [pins.tofLeft, pins.tofLeftDiag, pins.tofFront, pins.tofRightDiag, pins.tofRight]
# sensors = [VL6180X(), VL6180X(), VL6180X(), VL6180X(), VL6180X()]
# sensor_names = ["left", "leftDiag", "front", "rightDiag", "right"]


# self.sensor_pins = [pins.tofLeft, pins.tofRight]
# self.sensors = [VL6180X(), VL6180X()]
# sensor_names = ["left", "right"]

class Sensors:
  def __init__(self, pins, sensors, names):
    self._sensor_pins = pins
    self._sensors = sensors
    self._sensor_names = names
    

  def _initSensor(self, pin, sensor, address, sensor_name):
    digitalWrite(pin, HIGH) 
    sensor.default_settings()
    sensor.set_address(address)
    Serial.print("%s connected", sensor_name)

  def setup(self):
  	print("Initializing:\n");

  	# Sets all sensors to low for initialization
  	for pin in self._sensor_pins: 
    	digitalMode(pin, OUTPUT);
    	digitalWrite(pin, LOW);

  	# Initializes sensors
  	for i in range (len(self._sensor_pins)):
    	self._initSensor(self._sensor_pins[i], self._sensors[i], i + 1, self.sensor_names[i]);

  def test(self):
  	for i in range(len(self.sensor_pins)):
  	  print("%s: %i mm\n", self._sensor_names[i], self._sensors[i].get_distance)

	    sleep(10)

sensors = Sensors([pins.tofLeft, pins.tofRight], [VL6180X(), VL6180X()], ["left", "right"]
sensors.setup()
sensors.test()






