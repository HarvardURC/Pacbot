"""
    A motor, sensor, and PID test.
    Directs the robot to maintain a position equal to a specified 
    distance from a stationary or moving wall.

    Borrowed from the micromouse directory at https://github.com/HarvardURC/Micromouse/blob/master/2017%2C2018/tests/wall_follow_test/wall_follow_test.ino
"""
from pins import *
from GPIOhelpers import *
from sensors import Sensors
from motor import *
from PID import *

testing_distance = 50
min_num = 180


def main():
    timer = Timer()

    input = 0

    setpoint = testing_distance

    my_PID = PID(input, setpoint, 2.0, 0.0018, 0, DIRECT, timer)

    sensors = Sensors([pins.tof_front], ["rfront"],[0x29])

    left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l)
    right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r)

    my_PID.set_output_limits(-50, 50)

    my_PID.set_mode(AUTOMATIC)

    while(True):
	distance = sensors[0].get_distance()
        if my_PID.compute(distance,setpoint):
            if my_PID.output() >= 0:
                direction = MotorDirection.FORWARD
            else:
                direction = MotorDirection.BACKWARD

            power = abs(my_PID.output()) * 2

            left_motor.move(direction, power)
            right_motor.move(direction, power)

            print("Sensor: ")
            input = sensors["right"].get_distance()
            print(input)
            print(" Setpoint: ")
            print(Setpoint)

main()







