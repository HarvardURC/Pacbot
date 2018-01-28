from GPIOhelpers import *
from enum import Enum

class MotorDirection(Enum):
    BACKWARD = 0
    FORWARD = 1
    STOP = 2

class Motor:
    def __init__(self, name, power_pin, direction_pin, speed = 0):
        self.name = name
        self.power_pin = power_pin
        self.direction_pin = direction_pin
        self.speed = speed
        analogMode(self.power_pin, 0)
        digitalMode(self.direction_pin, OUTPUT)

    def move(self, direction, speed = self.speed):
        if direction == MotorDirection.STOP:
            analogWrite(self.power_pin, 0)
        else:
            print(str(self.name))
            print(" motor moving ")
            if direction == MotorDirection.BACKWARD:
                print("backwards")
            else:
                print("forwards")
            print("...\n")

            digitalWrite(self.direction_pin, direction)
            analogWrite(self.power_pin, speed)
            
