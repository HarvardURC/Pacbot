from motor import Motor, MotorDirection
from encoders import Encoder
from pins import *
from sensors import Sensors
from GPIOhelpers import *
from PID import *
setGPIO()

MOTOR_SPEED = 2
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
        self._rrightIR = self.sensors.sensors["rright"]

        self.encoderLeft = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
        self.encoderRight = Encoder(pins.encoder_pin_r1, pins.encoder_pin_r2)

        self.left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 0)

        self.setpointL = 0
        self.inputL = 0
        self.PIDLeft = PID(self.inputL, self.setpointL, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDLeft.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDLeft.set_mode(AUTOMATIC)
        
        self.setpointR = 0
        self.inputR = 0
        self.PIDRight = PID(self.inputR, self.setpointR, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDRight.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDRight.set_mode(AUTOMATIC)

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
        print("done")

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

        while ((abs(self.inputL - self.setpointL) > 5 or abs(self.inputR - self.setpointR) > 5) and (self.PIDRight.millis() - time < 20000)):
            self.inputL = abs(self.encoderLeft.read())
            self.inputR = abs(self.encoderRight.read())
            print(self.inputL)
            print(self.inputR)
            self.PIDRight.compute(self.inputR, self.setpointR)
            self.PIDLeft.compute(self.inputL, self.setpointL)

            l_rem = abs(self.inputL - self.setpointL)
            r_rem = abs(self.inputR - self.setpointR)

            if l_rem > r_rem :
                self.move_motors(self.PIDLeft.output(),0)

                print("left")
            elif r_rem > l_rem:
                self.move_motors(0,self.PIDRight.output())
                print("right")
            else:
                self.move_motors(self.PIDLeft.output(),self.PIDRight.output()) 
                print("both")
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

M = Motors()
M.forward()
M.stop()
from time import sleep
sleep(5)
#M.turn_left()
#M.stop()
#M.turn_right()
#M.stop()






