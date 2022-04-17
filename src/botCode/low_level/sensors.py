import sys
from time import sleep
from .pins import *
from .tofSensor import TofSensor
from .GPIOhelpers import *

setGPIO()

class Sensors:
    def __init__(self, pins_i, names, addresses):
        self.sensors = {}
        for pin in pins_i:
            digitalMode(pin, OUTPUT)
            digitalWrite(pin, LOW)
        
        for i, pin in enumerate(pins_i):
            self.sensors[names[i]] = TofSensor(pin, names[i], addresses[i])
            #a = input("enter chip")

        # for pin in pin_ce:
        #     digitalMode(pin, OUTPUT)
        #     digitalWrite(pin, LOW)

        # for i, pin in enumerate(pin_ce):
        #     digitalWrite(pin, LOW) 
        #     sleep(1)
        #     self.sensors[name[i]].set_address(addresses[i])

        # Initializes sensors
        for sensor_name in self.sensors:
            self.sensors[sensor_name].setup()

    def print_sensor_value(self, name):
        print("{}: {} mm".format(name, self.sensors[name].get_distance()))

    def print_all_values(self):
        for sensor_name in self.sensors:
            self.print_sensor_value(sensor_name)
