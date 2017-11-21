from motor import Motor, MotorDirection
from pins import *
from time import sleep

def test():
    left_motor = Motor("Left", pins.motor_power_l, pins.motor_direction_l)
    right_motor = Motor("Right", pins.motor_power_r, pins.motor_direction_r)

    print("Motors Initialized.\n")

    right_motor.move(MotorDirection.BACKWARD)
    sleep(1)
    right_motor.move(MotorDirection.FORWARD)
    sleep(1)
    right_motor.move(MotorDirection.BACKWARD)
    sleep(1)

    left_motor.move(MotorDirection.BACKWARD)
    sleep(1)
    left_motor.move(MotorDirection.FORWARD)
    sleep(1)
    left_motor.move(MotorDirection.BACKWARD)
    sleep(1)

    
    right_motor.move(MotorDirection.BACKWARD)
    left_motor.move(MotorDirection.BACKWARD)
    sleep(1)
    right_motor.move(MotorDirection.FORWARD)
    left_motor.move(MotorDirection.FORWARD)
    sleep(1)
    right_motor.move(MotorDirection.BACKWARD)
    left_motor.move(MotorDirection.BACKWARD)
    sleep(1)

test()
