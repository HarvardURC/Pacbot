from pins import *
from GPIOhelpers import *
from time import sleep

FORWARD = 0
BACKWARD = 1
STOP = -1

class Motor:
	def __init__(self, name, powerPin, directionPin):
    self.name = name
    self.powerPin = powerPin
    self.directionPin = directionPin

speed = 100
time = 1000

def move(motors, direction):
	for motor in motors:
		if direction == STOP:
			analogWrite(motor.powerPin, 0)

		else:
			print(str(motor.name))
			print(" motor moving ")
			if direction == 1:
				print("backwards")
			else:
				print("forwards")
			print("...\n")

			analogWrite(motor.powerPin, speed)
			digitalWrite(motor.directionPin, direction)
	sleep(1)



def setup():
	leftMotor = Motor("Left", pins.motorPowerL, pins.motorDirectionL)
	rightMotor = Motor("Right", pins.motorPowerL, pins.motorDirectionL)

	analogMode(pins.motorPowerL, 0)
	digitalMode(pins.motorDirectionL, OUTPUT)
	analogMode(pins.motorPowerR, 0)
	digitalMode(pins.motorDirectionR, OUTPUT)

	print("Motors Initialized.\n")

	move([rightMotor], BACKWARD)
	move([rightMotor], FORWARD)
	move([rightMotor], STOP)

	move([leftMotor], BACKWARD)
	move([leftMotor], FORWARD)
	move([leftMotor], STOP)

	move([rightMotor, leftMotor], BACKWARD)
	move([rightMotor, leftMotor], FORWARD)
	move([rightMotor, leftMotor], STOP)

setup()

