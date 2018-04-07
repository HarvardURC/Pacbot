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
from time import sleep
testing_distance = 50
min_num = 180


def main():
    timer = Timer()

    input = 0

    setpoint = testing_distance

    my_PID = PID(input, setpoint, 2.0, 0.002, 0.000, DIRECT, timer)

    sensors = Sensors([pins.tof_front], ["front"],[0x30])

    left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l)
    right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r)

    my_PID.set_output_limits(-10, 10)

    my_PID.set_mode(AUTOMATIC)

    while(True):
        distance = sensors.sensors["front"].get_distance() 
        if my_PID.compute(distance,setpoint):
            print("Output")
            print(my_PID.output())
            if my_PID.output() >= 0:
                direction = MotorDirection.FORWARD
                power = abs(my_PID.output()) * 2 
            else:
                direction = MotorDirection.BACKWARD
                power = abs(my_PID.output()) * 2 

            

            left_motor.move(direction, power)
            right_motor.move(direction, power)

            print("Sensor: ")
            input = sensors.sensors["front"].get_distance()
            print(input)
            print("...")
            #print(" Setpoint: ")
            #print(setpoint)
            sleep(0.1)

main()







