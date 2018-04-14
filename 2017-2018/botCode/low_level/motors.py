from motor import Motor, MotorDirection
from encoders import Encoder
from pins import *
from sensors import Sensors
from GPIOhelpers import *

setGPIO()

MOTOR_SPEED = 10
TICKS_CELL = 500
TICKS_TURN = 200

class Motors:
    def __init__(self):
        self.sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright,pins.tof_rleft,pins.tof_rright], ["front", "rear","fleft","fright","rleft","rright"], [0x30,0x31,0x32,0x33,0x34,0x35])
        self._frontIR = self.sensors.sensors["front"]
        self._fleftIR = self.sensors.sensors["fleft"]
        self._frightIR = self.sensors.sensors["fright"]
        self._rearIR = self.sensors.sensors["rear"]
        self._rleftIR = self.sensors.sensors["rleft"]
        self._rrightIR = rself.sensors.sensors["rright"]

        self.encoderLeft = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
        self.encoderRight = Encoder(pins.encoder_pin_r1, pins.encoder_pin_r2)

        self.left_motor = Motor("Left", pins.motor_power_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_power_r, pins.motor_direction_r, 0)

        self.setpointL = 0
        self.inputL = 0
        self.PIDLeft = PID(input, setpoint, 2.0, 0.002, 0.000, DIRECT, timer)
        self.PIDLeft.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDLeft.my_PID.set_mode(AUTOMATIC)
        
        self.setpointR = 0
        self.inputR = 0
        self.PIDRight = PID(input, setpoint, 2.0, 0.002, 0.000, DIRECT, timer)
        self.PIDRight.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDRight.my_PID.set_mode(AUTOMATIC)

    def move_motors(self, left, right):
        if left >= 0:
            self.left_motor.move(MotorDirection.FORWARD, ans(left))
        else:
            self.left_motor.move(MotorDirection.BACKWARD, ans(left))
        if right >= 0:
            self.right_motor.move(MotorDirection.FORWARD, ans(right))
        else:
            self.right_motor.move(MotorDirection.BACKWARD, ans(right))

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()

    def wait(self, ms):
        delay(ms/1000)

    def move_ticks(self, ticks_l, ticks_r):
        self.encoderLeft.write(0)
        self.encoderRight.write(0)

        self.setpointL = ticks_l
        self.setpointR = ticks_r

        self.inputR = 0
        self.inputL = 0

        time = self.PIDRight.millis()

        while ((abs(self.inputL - self.setpointL) > 10 or abs(self.inputR - self.setpointR) > 10) and (self.PIDRight.millis() - time < 2000)):
            self.inputL = self.encoderLeft.read()
            self.inputR = self.encoderRight.read()

            self.PIDRight(self.inputR, self.setpointR)
            self.PIDLeft(self.inputL, self.setpointL)

            l_rem = abs(self.inputL - self.setpointL)
            r_rem = abs(self.inputR - self.setpointR)

            if l_rem > r_rem :
                self.move_motors(self.PIDLeft.output(),0)
            elif r_rem > l_rem:
                self.move_motors(0,self.PIDRight.output())
            else:
                self.move_motors(self.PIDLeft.output(),self.PIDRight.output()) 
        self.stop()


    def forward(self):
        self.PIDLeft.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDRight.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDLeft.set_tunings(0.6,0.01,0.01)
        self.PIDRight.set_tunings(0.6,0.01,0.01)

        self.move_ticks(TICKS_CELL, TICKS_CELL)

    def turn_around_l():
        self.turn_left()
        self.turn_left()

    def turn_around_r():
        self.turn_right()
        self.turn_right()

    def turn_left(self): 
        # if self._frontIR.get_distance() < WALL_THRESHOLD:
        #     self.front_align()
        self.PIDLeft.set_tunings(1.7,0.01,0)
        self.PIDRight.set_tunings(1.7,0.01,0)
        self.move_ticks(-1 * TICKS_TURN, TICKS_TURN)

    def turn_right(self):
        # if self._frontIR.get_distance() < WALL_THRESHOLD:
        #     self.front_align()
        self.PIDLeft.set_tunings(1.7,0.01,0)
        self.PIDRight.set_tunings(1.7,0.01,0)
        self.move_ticks(TICKS_TURN, -1 * TICKS_TURN)

    # def front_align():



    def followTicksRight(self, ticks):
        self.encoderLeft.write(0)
        self.encoderRight.write(0)

        distance_l = 0
        distance_r = 0

        self.PIDLeft.set_tunings(0.6,0.01,0.01)

        while(distance_r + distance_l < ticks * 2):
            distance_l = self.encoderLeft.read()
            distance_r = self.encoderRight.read()
            # self.inputR = self.right
            # self.setpointR = 
            self.PIDRight.compute(self.inputR, self.setpointR)

            outputR = self.PIDRight.output()

            self.move_motors()

        offset = (distance_l - distance_r)/2
        self.move_ticks(-1 * offset, offset)
        self.stop()


        






