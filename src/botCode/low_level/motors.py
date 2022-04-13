from motor import Motor, MotorDirection
from pins import *
from sensors import Sensors
from GPIOhelpers import *
from PID import *
setGPIO()
import time
import signal, sys

from teensySensors import TeensySensors

from time import sleep


MOTOR_SPEED = 25 
TICKS_CELL = 390

TIME = 3000
KP = 0.4
KI = 0.01
KD = 0.05

class Motors:
    def __init__(self):
        self.teensy_sensors = TeensySensors()
        sleep(2)
        
        #self.ir_sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright,pins.tof_rleft,pins.tof_rright], ["front", "rear","fleft","fright","rleft","rright"], [0x30,0x31,0x32,0x33,0x34,0x35])
        #self._frontIR = self.ir_sensors.sensors["front"]
        #self._fleftIR = self.ir_sensors.sensors["fleft"]
        #self._frightIR = self.ir_sensors.sensors["fright"]
        #self._rearIR = self.ir_sensors.sensors["rear"]
        #self._rleftIR = self.ir_sensors.sensors["rleft"]
        #self._rrightIR = self.ir_sensors.sensors["rright"]

        self.directions = ["N", "E", "S", "W"]
        self.cur_dir = 0
        self.heading = {"E": 0, "N": 90, "W": 180, "S": 270}


        self.left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 0)

        self.setpointHeading = 0
        self.inputStraight = 0
        self.PIDHeading = PID(self.inputStraight, self.setpointHeading, KP, KI, KD, DIRECT, Timer)
        self.PIDHeading.set_output_limits(-1*(100 - MOTOR_SPEED), 100 - MOTOR_SPEED)
        self.PIDHeading.set_mode(AUTOMATIC)

        self.setpointTurnHeading = 0
        self.inputTurn = 0
        self.PIDTurn = PID(self.inputTurn, self.setpointHeading, 0.2, 0, 0, DIRECT, Timer)
        self.PIDTurn.set_output_limits(-1*MOTOR_SPEED, MOTOR_SPEED)
        self.PIDTurn.set_mode(AUTOMATIC)

        self.reset_heading()

    def read_encoders(self):
        return self.teensy_sensors.get_left_encoder_ticks(), self.teensy_sensors.get_right_encoder_ticks()

    def reset_heading(self):
        current_heading = self.teensy_sensors.get_heading()

        for i in range(4):
            self.heading[(self.cur_dir + i)] = (current_heading + (i * 90)) % 360



    def move_motors(self, left, right):
        if left >= 0:
            self.left_motor.move(MotorDirection.FORWARD, abs(left))
        else:
            self.left_motor.move(MotorDirection.BACKWARD, abs(left))
        if right >= 0:
            self.right_motor.move(MotorDirection.FORWARD, abs(right))
        else:
            self.right_motor.move(MotorDirection.BACKWARD, abs(right))

    def stop(self):
        print("stopped")
        self.right_motor.stop()
        self.left_motor.stop()
    
    def move_cells(self, cells):
        self.drive_straight(self.heading[self.cur_dir], cells*TICKS_CELL)
    
    def drive_straight(self, heading, ticks):
        self.teensy_sensors.reset_encoders()
        self.setpointHeading = heading

        factor = ticks/TICKS_CELL
        distance_l, distance_r = 0, 0 
       
        while min(distance_r, distance_l) < ticks:
        #while 1:
            # might wanna add logic to avoid hitting wall

            # logic to add distance for more time to straighten out
            # if abs(distance_l - distance_r) > 140:
            #     print('added: {}'.format(added))
            #     added += 4
            #     ticks += 4
            distance_l, distance_r = self.read_encoders()
            #print("Distance:", distance_l, distance_r)

            self.inputStraight = self.teensy_sensors.get_heading()
            
            # Only undergo PID ever 0.1 second
            last_set = time.time()
            # Compute error
            error = self.compute_heading_error(self.inputStraight, self.setpointHeading)
            self.PIDHeading.compute(error, 0)
            #print("Error:", error, " Pid heading:", self.PIDHeading.output())
            self.move_motors((MOTOR_SPEED + self.PIDHeading.output()), (MOTOR_SPEED - self.PIDHeading.output()))
            sleep(0.1)

    def reverse(self, ticks):
        self.reverse_direction()
        self.move_cells(ticks)
        self.reverse_direction()

    def back(self):
        if(self._rearIR.get_distance() > 25 and self._rleftIR.get_distance()> 10 and self._rrightIR.get_distance() > 10):
            print("back")
            self.move_ticks(-TICKS_CELL/4, -TICKS_CELL/4)
        else:
            print("not back")
 

    def turn_around(self):
        self.cur_dir = (self.cur_dir + 2) % 4
        self.turn_to_direction(self.heading[self.cur_dir])

    def compute_heading_error(self, cur, des):
        return (cur - des + 540) % 360 - 180

    def turn_to_direction(self, heading):
        self.inputTurn = self.compute_heading_error(self.teensy_sensors.get_heading(), heading)
        self.setpointTurnHeading = 0
        while abs(self.inputTurn) > 0.5:
            self.move_motors(self.PIDTurn.output(), -self.PIDTurn.output())
            self.inputTurn = self.compute_heading_error(self.teensy_sensors.get_heading(), heading)
            self.PIDTurn.compute(self.inputTurn, self.setpointTurnHeading)


    def turn_left(self):
        self.cur_dir = (self.cur_dir + 1)%4
        self.turn_to_direction(self.heading[self.cur_dir])
    
    def turn_right(self):
        self.cur_dir = (self.cur_dir - 1)%4
        self.turn_to_direction(self.heading[self.cur_dir])

    def straight(self):
        #print("straight")
        if self.dir:
            self.move_motors(MOTOR_SPEED/2, MOTOR_SPEED/2)
        else:
            self.move_motors(-MOTOR_SPEED/2, -MOTOR_SPEED/2)
