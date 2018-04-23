from .ST_VL6180X import VL6180X
from .GPIOhelpers import *
setGPIO()

class TofSensor:
    def __init__(self, pin, name, address):
        self.name = name
        self.address = address
        self.pin = pin
        
        digitalMode(self.pin, INPUT_PULLUP)

        self.sensor = VL6180X()
        self.sensor.set_address(self.address)
        #digitalMode(self.pin, LOW)
        #self.setup()
	#self.sensor.set_address(self.address)

    def setup(self):
        #digitalWrite(self.pin, INPUT_PULLUP)
        self.sensor.default_settings()
        #self.sensor.set_address(self.address)
        print("{} connected".format(self.name))

    def set_address(self, address):
        self.sensor.set_address(address)

    def get_distance(self):
        return self.sensor.get_distance()
