from low_level.motor import Motor, MotorDirection
from low_level.pins import *
from time import sleep
from low_level.motors import Motors
from low_level.motors import Direction
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
    if True:
        motors.move_cells(6)
        motors.turn_left()
        motors.move_cells(3)
        motors.turn_left()
        motors.move_cells(6)
        motors.turn_right()

def test_advance_left():
    motors = Motors()
    motors.move_cells(1)
    motors.turn_left()

def test_turn_right():
    motors = Motors()
    motors.turn_right()

def test_turn_left():
    motors = Motors()
    motors.turn_left()

def test_reverse():
    motors = Motors()
    motors.reverse_direction()

def test_drive_forward_till_clear():
    motors = Motors()
    motors.driveForwardTillClear(motors._rleftIR)

def test_drive_in_direction_north():
    motors = Motors()
    motors.drive_in_direction(Direction.N, 1)


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
    elif "-10" in sys.argv:
        test_advance_left()
    elif "-11" in sys.argv:
        test_turn_right()
    elif "-12" in sys.argv:
        test_turn_left()
    elif "-13" in sys.argv:
        test_reverse_direction()
    elif "-14" in sys.argv:
        test_drive_forward_till_clear()
    elif "-15" in sys.argv:
        test_drive_in_direction_north()
    else:
        test()
