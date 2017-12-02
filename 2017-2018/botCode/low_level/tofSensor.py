from ST_VL6180X import VL6180X
from GPIOhelpers import *
setGPIO()

class TofSensor:
    def __init__(self, pin, name, address):
        self.name = name
        self.sensor = VL6180X(address = address)
        self.pin = pin
        digitalMode(self.pin, OUTPUT)
        digitalWrite(self.pin, LOW)

    def setup(self):
        digitalWrite(self.pin, HIGH)
        self.sensor.default_settings()
        # sensor.set_address(address)
        print("{} connected".format(self.name))

    def get_distance(self):
        return self.sensor.get_distance()
