import sys
from time import sleep
from pins import *
from tofSensor import TofSensor
# from GPIOhelpers import *

# setGPIO()

class Sensors:
    def __init__(self, pins, names, addresses):
        self.sensors = {}
        
        for i, pin in enumerate(pins):
            self.sensors[names[i]] = TofSensor(pin, names[i], addresses[i])

        # Initializes sensors
        for sensor_name in self.sensors:
            self.sensors[sensor_name].setup()

    def print_sensor_value(self, name):
        print("{}: {} mm\n".format(name, self.sensors[name].get_distance()))

    def print_all_values(self):
        for sensor_name in self.sensors:
            self.print_sensor_value(sensor_name)
