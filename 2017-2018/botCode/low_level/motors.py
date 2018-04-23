from .motor import Motor, MotorDirection
from .encoders import Encoder
from .pins import *
from .sensors import Sensors
from .GPIOhelpers import *
from .PID import *
setGPIO()

import signal, sys

MOTOR_SPEED = 10
TICKS_CELL = 500
TICKS_TURN = 300
WALL_THRESHOLD_DIAG = 85
WALL_DISTANCE_DIAG = 70
WALL_DIST = 80
KP3 = 0.4
KP = .4
KP2 = .4
KI = 0.01
KD = 0.05
class Motors:
    def __init__(self):
        self.sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright,pins.tof_rleft,pins.tof_rright], ["front", "rear","fleft","fright","rleft","rright"], [0x30,0x31,0x32,0x33,0x34,0x35])
        self._frontIR = self.sensors.sensors["front"]
        self._fleftIR = self.sensors.sensors["fleft"]
        self._frightIR = self.sensors.sensors["fright"]
        self._rearIR = self.sensors.sensors["rear"]
        self._rleftIR = self.sensors.sensors["rleft"]
        self._rrightIR = self.sensors.sensors["rright"]

        self.dir = True

        self.encoderLeft = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
        self.encoderRight = Encoder(pins.encoder_pin_r1, pins.encoder_pin_r2)

        self.left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 0)

        self.setpointL = 0
        self.inputL = 0
        self.PIDLeft = PID(self.inputL, self.setpointL, KP3, 0.002, 0.000, DIRECT, Timer)
        self.PIDLeft.set_output_limits(-1 * MOTOR_SPEED/10, MOTOR_SPEED/10)
        self.PIDLeft.set_mode(AUTOMATIC)

        self.setpointR = 0
        self.inputR = 0
        self.PIDRight = PID(self.inputR, self.setpointR, KP3, 0.002, 0.000, DIRECT, Timer)
        self.PIDRight.set_output_limits(-1 * MOTOR_SPEED/10, MOTOR_SPEED/10)
        self.PIDRight.set_mode(AUTOMATIC)

        self.setpointfL = 0
        self.inputfL = 0
        self.PIDfLeft = PID(self.inputfL, self.setpointfL, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDfLeft.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDfLeft.set_mode(AUTOMATIC)
        
        self.setpointfR = 0
        self.inputfR = 0
        self.PIDfRight = PID(self.inputfR, self.setpointfR, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDfRight.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDfRight.set_mode(AUTOMATIC)

        self.setpointrL = 0
        self.inputrL = 0
        self.PIDrLeft = PID(self.inputrL, self.setpointrL, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDrLeft.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDrLeft.set_mode(AUTOMATIC)
        
        self.setpointrR = 0
        self.inputrR = 0
        self.PIDrRight = PID(self.inputrR, self.setpointrR, 2.0, 0.002, 0.000, DIRECT, Timer)
        self.PIDrRight.set_output_limits(-1 * MOTOR_SPEED, MOTOR_SPEED)
        self.PIDrRight.set_mode(AUTOMATIC)

    def read_encoders(self):
        if self.dir:
            return (self.encoderLeft.read(), -self.encoderRight.read())
        else:
            return (-self.encoderLeft.read(), self.encoderRight.read())

    def raw_encoders(self):
        return (self.encoderLeft.read(), self.encoderRight.read())

    def reverse_direction(self):
        self.dir = not self.dir

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

    def move_ticks(self, ticks_l, ticks_r):
        self.encoderLeft.write(0)
        self.encoderRight.write(0)

        self.setpointL = ticks_l
        self.setpointR = ticks_r

        self.inputR = 0
        self.inputL = 0

        time = self.PIDRight.millis()

        while (abs(self.inputL - self.setpointL) > 5 or abs(self.inputR - self.setpointR) > 5):
            self.inputL , self.inputR = self.read_encoders()
            print(self.inputL)
            print(self.inputR)

            self.PIDRight.compute(self.inputR, self.setpointR)
            self.PIDLeft.compute(self.inputL, self.setpointL)

            l_rem = abs(self.inputL - self.setpointL)
            r_rem = abs(self.inputR - self.setpointR)
            
            if l_rem > r_rem :
                self.move_motors(self.PIDLeft.output(),0)
            elif r_rem > l_rem:
                self.move_motors(0,self.PIDRight.output())
            else:
                self.move_motors(self.PIDLeft.output(),self.PIDRight.output()) 
            
        self.stop()

    def advance(self, ticks):
        self.encoderLeft.write(0)
        self.encoderRight.write(0)

        distance_l, distance_r = self.read_encoders()

        while (distance_l + distance_r < ticks * 2):
            distance_l, distance_r = self.read_encoders()
            print(distance_l)
            print(distance_r)
            dists = {
                'fr': self._frightIR.get_distance(),
                'fl': self._fleftIR.get_distance(),
                'rr': self._rrightIR.get_distance(),
                'rl': self._rleftIR.get_distance()
            }

            front_valid = dists['fr'] < WALL_THRESHOLD_DIAG and dists['fl'] < WALL_THRESHOLD_DIAG and (dists['fr'] < WALL_DIST or dists['fl'] < WALL_DIST)
            rear_valid = dists['rr'] < WALL_THRESHOLD_DIAG and dists['rl'] < WALL_THRESHOLD_DIAG and (dists['rr'] < WALL_DIST or dists['rl'] < WALL_DIST)
            left_valid = dists['fl'] <  WALL_THRESHOLD_DIAG and dists['rl'] <  WALL_THRESHOLD_DIAG and (dists['fl'] <  WALL_DIST or dists['rl'] <  WALL_DIST)
            right_valid = dists['fr'] <  WALL_THRESHOLD_DIAG and dists['rr'] <  WALL_THRESHOLD_DIAG and (dists['fr'] <  WALL_DIST or dists['rr'] <  WALL_DIST)

            max2 = max(dists, key = lambda k: dists[k] if dists[k] < WALL_THRESHOLD_DIAG else -float('inf'))
            single_sensor_functions = {
                    'fr': self.follow_front_right,
                    'fl': self.follow_front_left,
                    'rr': self.follow_rear_right,
                    'rl': self.follow_rear_left
            }

            if front_valid:
                """
                if rear_valid:
                    front_min = min(dists['fr'], dists['fl'])
                    rear_min = min(dists['rr'], dists['rl'])
                    if front_min <= rear_min:
                        self.follow_front()
                    else:
                        self.follow_rear()
                else:
                    self.follow_front()
                """
                self.follow_front()
            #elif rear_valid:
                #self.follow_rear()
            elif left_valid:
                self.follow_left()
            elif right_valid:
                self.follow_right()
                
            elif dists[max2] < WALL_THRESHOLD_DIAG:
                single_sensor_functions[max2]()
            else:
                self.straight()

        #offset = (distance_l - distance_r)/2
        #self.move_ticks(-1 * offset, offset)
        self.stop()

    def reverse(self, ticks):
        self.reverse_direction()
        self.advance(ticks)
        self.reverse_direction()

    def turn_around_l(self):
        self.turn_left()
        self.turn_left()

    def turn_around_r(self):
        self.turn_right()
        self.turn_right()

    def turn_left(self): 
        # if self._frontIR.get_distance() < WALL_THRESHOLD:
        #     self.front_align()
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        self.move_ticks(-1 * TICKS_TURN, TICKS_TURN)

    def turn_right(self):
        # if self._frontIR.get_distance() < WALL_THRESHOLD:
        #     self.front_align()
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        self.move_ticks(TICKS_TURN, -1 * TICKS_TURN)

    # def front_align():

    def follow_front(self):
        print("fFront")
        self.PIDfLeft.set_tunings(KP, KI, KD)
        self.PIDfRight.set_tunings(KP, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG
        self.setpointfL = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()
        self.inputfL = self._fleftIR.get_distance()

        self.PIDfRight.compute(self.inputfR, self.setpointfR)
        self.PIDfLeft.compute(self.inputfL, self.setpointfL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED + self.PIDfRight.output())/2)
        else: 
            self.move_motors(-(MOTOR_SPEED + self.PIDfLeft.output())/2, -(MOTOR_SPEED + self.PIDfRight.output())/2)

    def follow_rear(self):
        print("fRear")

        self.PIDrLeft.set_tunings(KP, KI, KD)
        self.PIDrRight.set_tunings(KP, KI, KD)
        self.setpointrR = WALL_DISTANCE_DIAG
        self.setpointrL = WALL_DISTANCE_DIAG

        self.inputrR = self._rrightIR.get_distance()
        self.inputrL = self._rleftIR.get_distance()
        

        self.PIDrRight.compute(self.inputrR, self.setpointrR)
        self.PIDrLeft.compute(self.inputrL, self.setpointrL)

        if self.dir:
            self.move_motors((MOTOR_SPEED - self.PIDrLeft.output())/2, (MOTOR_SPEED - self.PIDrRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDrLeft.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)

    def follow_left(self):
        print("fLeft")

        self.PIDfLeft.set_tunings(KP, KI, KD)
        self.PIDrLeft.set_tunings(KP, KI, KD)
        self.setpointfL = WALL_DISTANCE_DIAG
        self.setpointrL = WALL_DISTANCE_DIAG


        self.inputfL = self._fleftIR.get_distance()
        self.inputrL = self._rleftIR.get_distance()

        self.PIDfLeft.compute(self.inputfL, self.setpointfL)
        self.PIDrLeft.compute(self.inputrL, self.setpointrL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED + self.PIDrLeft.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDfLeft.output())/2, -(MOTOR_SPEED + self.PIDrLeft.output())/2)

    def follow_right(self):
        print("fRight")

        self.PIDfRight.set_tunings(KP, KI, KD)
        self.PIDrRight.set_tunings(KP, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG
        self.setpointrR = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()
        self.inputrR = self._rrightIR.get_distance()              
            
        self.PIDfRight.compute(self.inputfR, self.setpointfR)
        self.PIDrRight.compute(self.inputrR, self.setpointrR)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfRight.output())/2, (MOTOR_SPEED + self.PIDrRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDfRight.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)

    def follow_front_right(self):
        print("ffRight")

        self.PIDfRight.set_tunings(KP2, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()

        self.PIDfRight.compute(self.inputfR, self.setpointfR)

        if self.dir:
            self.move_motors((MOTOR_SPEED - self.PIDfRight.output())/2, (MOTOR_SPEED + self.PIDfRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED - self.PIDfRight.output())/2, -(MOTOR_SPEED + self.PIDfRight.output())/2)

    def follow_front_left(self):
        print("ffLeft")

        self.PIDfLeft.set_tunings(KP2, KI, KD)
        self.setpointfL = WALL_DISTANCE_DIAG

        self.inputfL = self._fleftIR.get_distance()

        self.PIDfLeft.compute(self.inputfL, self.setpointfL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED - self.PIDfLeft.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDfLeft.output())/2, -(MOTOR_SPEED - self.PIDfLeft.output())/2)

    def follow_rear_right(self):
        print("frRight")

        self.PIDrRight.set_tunings(KP2, KI, KD)
        self.setpointrR = WALL_DISTANCE_DIAG

        self.inputrR = self._rrightIR.get_distance()

        self.PIDrRight.compute(self.inputrR, self.setpointrR)

        if self.dir:
            self.move_motors((MOTOR_SPEED - self.PIDrRight.output())/2, (MOTOR_SPEED + self.PIDrRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED - self.PIDrRight.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)

    def follow_rear_left(self):
        print("frLeft")

        self.PIDrLeft.set_tunings(KP2, KI, KD)
        self.setpointrL = WALL_DISTANCE_DIAG

        self.inputrL = self._rleftIR.get_distance()

        self.PIDrLeft.compute(self.inputrL, self.setpointrL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDrLeft.output())/2, (MOTOR_SPEED - self.PIDrLeft.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDrLeft.output())/2, -(MOTOR_SPEED - self.PIDrLeft.output())/2)


    def straight(self):
        print("straight")
        if self.dir:
            self.move_motors(MOTOR_SPEED/2, MOTOR_SPEED/2)
        else:
            self.move_motors(-MOTOR_SPEED/2, -MOTOR_SPEED/2)
'''
M = Motors()


#M.reverse_direction()
try:
   # M.advance(3000)
    M.turn_left()
    #M.advance(3000)
except KeyboardInterrupt:
    M.stop()
    sys.exit()

M.stop()
print("done")

import sys

sys.exit()
'''
