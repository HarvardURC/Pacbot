from motor import Motor, MotorDirection
from pins import *
from time import sleep

def test():
    left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 100)
    right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 100)

    print("Motors Initialized.\n")

    # right_motor.move(MotorDirection.BACKWARD)
    # sleep(1)
    # right_motor.move(MotorDirection.FORWARD)
    # sleep(1)
    # right_motor.move(MotorDirection.BACKWARD)
    # sleep(1)

    left_motor.move(MotorDirection.BACKWARD, 50)
    sleep(1)
    left_motor.stop()
    left_motor.move(MotorDirection.FORWARD, 50)
    sleep(1)
    left_motor.stop()
    left_motor.move(MotorDirection.BACKWARD,50)
    sleep(1)
    left_motor.stop()

    right_motor.move(MotorDirection.BACKWARD, 50)
    sleep(1)
    right_motor.stop()
    right_motor.move(MotorDirection.FORWARD, 50)
    sleep(1)
    right_motor.stop()
    right_motor.move(MotorDirection.BACKWARD,50)
    sleep(1)
    right_motor.stop()

    
    right_motor.move(MotorDirection.BACKWARD, 70)
    left_motor.move(MotorDirection.BACKWARD, 70)
    sleep(1)
    right_motor.stop()
    left_motor.stop()
    right_motor.move(MotorDirection.FORWARD, 40)
    left_motor.move(MotorDirection.FORWARD, 40)
    sleep(1)
    right_motor.stop()
    left_motor.stop()
    right_motor.move(MotorDirection.BACKWARD, 80)
    left_motor.move(MotorDirection.BACKWARD, 80)
    sleep(1)
    right_motor.stop()
    left_motor.stop()

test()
