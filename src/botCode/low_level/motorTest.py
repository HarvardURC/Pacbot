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
    right_motor.move(MotorDirection.FORWARD, 10)
    left_motor.move(MotorDirection.FORWARD, 10)
    
    sleep(5)
    right_motor.stop()
    left_motor.stop()

def test_drive_straight():
    motors = Motors()
    motors.drive_straight(110.38, 530)

def test_turn_to_heading():
    motors = Motors()
    motors.turn_to_direction(107.5)

def test_drive_turn():
    motors = Motors()
    motors.drive_straight(110.38, 530)
    motors.stop()
    motors.turn_to_direction(30)

def test_advance_one():
    motors = Motors()
    motors.move_cells(1)

def test_advance_four():
    motors = Motors()
    motors.move_cells(4)

def test_advance_two_then_turn_right():
    motors = Motors()
    motors.move_cells(2)
    motors.turn_right()
    motors.move_cells(2)
    motors.turn_left()

def test_advance_three():
    motors = Motors()
    motors.move_cells(3)

def test_advance_right():
    motors = Motors()
    motors.move_cells(3)
    motors.turn_right()
    motors.move_cells(2)
    motors.turn_left()
    motors.move_cells(3)

def test_advance_right_more():
    motors = Motors()
    motors.move_cells(3)
    motors.turn_right()
    motors.move_cells(2)
    motors.turn_left()
    motors.move_cells(3)
    motors.turn_left()
    motors.move_cells(5)
    motors.turn_right()

if __name__ == "__main__":
    if "-1" in sys.argv:
        test_drive_straight()
    elif "-2" in sys.argv:
        test_turn_to_heading()
    elif "-3" in sys.argv:
        test_drive_turn()
    elif "-4" in sys.argv:
        test_advance_one()
    elif "-5" in sys.argv:
        test_advance_four()
    elif "-6" in sys.argv:
        test_advance_two_then_turn_right()
    elif "-7" in sys.argv:
        test_advance_three()
    elif "-8" in sys.argv:
        test_advance_right()
    elif "-9" in sys.argv:
        test_advance_right_more()
    else:
        test()
