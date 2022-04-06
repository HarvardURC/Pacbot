from motor import Motor, MotorDirection
from pins import *
from time import sleep
from motors import Motors
import sys

def test():
    left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 100)
    right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 100)
    sleep(3)
    print("Motors Initialized.\n")
    sleep(1)
    right_motor.move(MotorDirection.FORWARD, 50)
    left_motor.move(MotorDirection.FORWARD, 50)
    
    sleep(5)
    right_motor.stop()
    left_motor.stop()

#test()


if __name__ == "__main__":
    if "-1" in sys.argv:
        motors = Motors()
        motors.driveStraight(336.44, 260)
    else:
        test()
