from .motor import Motor, MotorDirection
import Encoder
from .pins import *
from .sensors import Sensors
from .GPIOhelpers import *
from .PID import *
setGPIO()
import time
import signal, sys

MOTOR_SPEED = 47
TICKS_CELL = 260
TICKS_TURN = 231
WALL_THRESHOLD_DIAG = 85
WALL_DISTANCE_DIAG = 75
WALL_DIST = 80
TIME = 3000
KP3 = 0.5
KP = 0.4
KP2 = .17
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

        Encoder.init(pins.encoder_pin_l1, pins.encoder_pin_l2, 0)
        Encoder.init(pins.encoder_pin_r1, pins.encoder_pin_r2, 1)

        self.left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 0)

        self.setpointL = 0
        self.inputL = 0
        self.PIDLeft = PID(self.inputL, self.setpointL, KP3, 0.002, 0.000, DIRECT, Timer)
        self.PIDLeft.set_output_limits(-1 * MOTOR_SPEED*1.5, MOTOR_SPEED*1.5)
        self.PIDLeft.set_mode(AUTOMATIC)

        self.setpointR = 0
        self.inputR = 0
        self.PIDRight = PID(self.inputR, self.setpointR, KP3, 0.002, 0.000, DIRECT, Timer)
        self.PIDRight.set_output_limits(-1 * MOTOR_SPEED*1.5, MOTOR_SPEED*1.5)
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
            return (-Encoder.read(0), Encoder.read(1))
        else:
            return (Encoder.read(0), -Encoder.read(1))

    def raw_encoders(self):
        return (Encoder.read(0), Encoder.read(1))

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
        Encoder.write(0, 0)
        Encoder.write(0, 1)

        factor = abs(ticks_l)/TICKS_CELL

        self.setpointL = ticks_l
        self.setpointR = ticks_r

        self.inputR = 0
        self.inputL = 0

        start = time.time() * 1000
        while ((abs(self.inputL - self.setpointL) > 5 or abs(self.inputR - self.setpointR) > 5) and (time.time()* 1000 - start < factor *TIME)):
            self.inputL , self.inputR = self.read_encoders()
            #print(self.inputL)
            #print(self.inputR)

            self.PIDRight.compute(self.inputR, self.setpointR)
            self.PIDLeft.compute(self.inputL, self.setpointL)

            l_rem = abs(self.inputL - self.setpointL)
            r_rem = abs(self.inputR - self.setpointR)
            
            if l_rem > r_rem and (abs(l_rem - r_rem) > 10 or r_rem < 10):
                self.move_motors(self.PIDLeft.output(),0)
            elif r_rem > l_rem and (abs(l_rem - r_rem) > 10 or l_rem < 10):
                self.move_motors(0,self.PIDRight.output())
            else:
                self.move_motors(self.PIDLeft.output(),self.PIDRight.output()) 
            
        self.stop()
    
    def move_cells(self, cells):
        """for _ in range(cells):  
            self.advance(TICKS_CELL)
        """
        self.advance(cells*TICKS_CELL)
    def advance(self, ticks):
        Encoder.write(0, 0)
        Encoder.write(0, 1)

        factor = ticks/TICKS_CELL

        distance_l, distance_r = self.read_encoders()
        added = 0
        have_driven = False
        start = time.time()*1000
        while (min(distance_r, distance_l) < ticks and (time.time()*1000 - start < factor * TIME)):
            if have_driven and self.dir and self._frontIR.get_distance() < 40  and self._fleftIR.get_distance() < 65 and  self._frightIR.get_distance() < 65:
                print("break:",self._frontIR.get_distance())
                break
            elif have_driven and not self.dir and self._rearIR.get_distance() < 40 and (self._rleftIR.get_distance() < 65 or  self._rrightIR.get_distance() < 65):
                break
            
            if abs(distance_l - distance_r) > 140:
                print('added: {}'.format(added))
                added += 4
                ticks += 4
            distance_l, distance_r = self.read_encoders()
            #print(distance_l)
            #print(distance_r)
            dists = {
                'fr': self._frightIR.get_distance(),
                'fl': self._fleftIR.get_distance(),
                'rr': self._rrightIR.get_distance(),
                'rl': self._rleftIR.get_distance()
            }

            front_valid = dists['fr'] < WALL_THRESHOLD_DIAG and dists['fl'] < WALL_THRESHOLD_DIAG and (dists['fr'] < WALL_DIST or dists['fl'] < WALL_DIST)
            rear_valid = dists['rr'] < WALL_THRESHOLD_DIAG and dists['rl'] < WALL_THRESHOLD_DIAG and (dists['rr'] < WALL_DIST or dists['rl'] < WALL_DIST)
            left_valid = dists['fl'] <  WALL_THRESHOLD_DIAG and dists['rr'] <  WALL_THRESHOLD_DIAG and (dists['fl'] <  WALL_DIST or dists['rr'] <  WALL_DIST)
            right_valid = dists['fr'] <  WALL_THRESHOLD_DIAG and dists['rl'] <  WALL_THRESHOLD_DIAG and (dists['fr'] <  WALL_DIST or dists['rl'] <  WALL_DIST)

            if self.dir:
                max2 = min(dists, key = lambda k: dists[k] if (dists[k] < WALL_THRESHOLD_DIAG and k[0] != 'r') else float('inf'))
                single_sensor_functions = {
                        'fr': self.follow_front_right,
                        'fl': self.follow_front_left
                }
            else:
                max2 = min(dists, key = lambda k: dists[k] if (dists[k] < WALL_THRESHOLD_DIAG and k[0] != 'f') else float('inf'))
                single_sensor_functions = {
                        'rr': self.follow_rear_right,
                        'rl': self.follow_rear_left
                }

            if front_valid and self.dir:
                self.follow_front()
            elif rear_valid and not self.dir:
                self.follow_rear()
            elif dists[max2] < WALL_THRESHOLD_DIAG and max2[0] != 'r' and self.dir:
                #print(max2)
                single_sensor_functions[max2]()
            elif dists[max2] < WALL_THRESHOLD_DIAG and max2[0] != 'f' and not self.dir:
                single_sensor_functions[max2]()
            else:
                self.straight()
            have_driven = True
 
            """
            elif left_valid:
                self.follow_left()
            elif right_valid:
                print("right")
                self.follow_right()

            """ 
        self.stop()

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

    def turn_slight_left(self):
        print("turn_slight_left")
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        self.move_ticks(-1 * TICKS_TURN/6, TICKS_TURN/6)
    
    def turn_slight_right(self):
        print("turn_slight_right")
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        self.move_ticks(1 * TICKS_TURN/6, -1*TICKS_TURN/6)

    def attempt_escape(self):
        if(self._frontIR.get_distance() > 40 and self._fleftIR.get_distance()> 60 and self._frightIR.get_distance() > 60):
            print("attempted")
            self.move_cells(1)
            return True
        else:
            print("could not")
            return False

    def escape(self):
        escaped = False
        self.dir = True
        if self._frightIR.get_distance() <= self._fleftIR.get_distance():
            while not escaped:
                print('stuck')
                self.back()
                self.turn_slight_left()
                escaped = self.attempt_escape()
            if(self._frontIR.get_distance() < 40  or self._fleftIR.get_distance() < 10 or self._frightIR.get_distance() < 10):
                print("second escape")
                self.turn_left()
                self.move_cells(2)
        else: 
            while not escaped:
                print('stuck')
                self.back()
                self.turn_slight_right()
                escaped = self.attempt_escape()
            if(self._frontIR.get_distance() < 40  or self._fleftIR.get_distance() < 10 or self._frightIR.get_distance() < 10):
                print("second escape")
                self.turn_right()
                self.move_cells(2)
 

    def turn_around_l(self):
        self.turn_left()
        self.turn_left()

    def turn_around_r(self):
        self.turn_right()
        self.turn_right()

    def turn_left(self): 
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        if self.dir:
            self.move_ticks(-1 * TICKS_TURN, TICKS_TURN)
        else: 
            self.move_ticks(TICKS_TURN, -1*TICKS_TURN)
            self.reverse_direction()

    def turn_right(self):
        self.PIDLeft.set_tunings(KP3,0.01,0)
        self.PIDRight.set_tunings(KP3,0.01,0)
        if self.dir:
            self.move_ticks(TICKS_TURN, -1 * TICKS_TURN)
        else: 
            self.move_ticks(-1 * TICKS_TURN, TICKS_TURN)
            self.reverse_direction()

    def follow_front(self):
        #print("fFront")
        self.PIDfLeft.set_tunings(KP, KI, KD)
        self.PIDfRight.set_tunings(KP, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG
        self.setpointfL = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()
        self.inputfL = self._fleftIR.get_distance()

        self.PIDfRight.compute(self.inputfR, self.setpointfR)
        self.PIDfLeft.compute(self.inputfL, self.setpointfL)


        self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED + self.PIDfRight.output())/2)
        

    def follow_rear(self):
        #print("fRear")

        self.PIDrLeft.set_tunings(KP, KI, KD)
        self.PIDrRight.set_tunings(KP, KI, KD)
        self.setpointrR = WALL_DISTANCE_DIAG
        self.setpointrL = WALL_DISTANCE_DIAG

        self.inputrR = self._rrightIR.get_distance()
        self.inputrL = self._rleftIR.get_distance()
        
        #print("R:",self.inputrR)
        #print("L:",self.inputrL)
        self.PIDrRight.compute(self.inputrR, self.setpointrR)
        self.PIDrLeft.compute(self.inputrL, self.setpointrL)


        self.move_motors(-(MOTOR_SPEED + self.PIDrLeft.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)
            

    def follow_left(self):
        #print("fLeft")

        self.PIDfLeft.set_tunings(KP, KI, KD)
        self.PIDrLeft.set_tunings(KP, KI, KD)
        self.setpointfL = WALL_DISTANCE_DIAG
        self.setpointrR = WALL_DISTANCE_DIAG


        self.inputfL = self._fleftIR.get_distance()
        self.inputrR = self._rrightIR.get_distance()

        self.PIDfLeft.compute(self.inputfL, self.setpointfL)
        self.PIDrRightt.compute(self.inputrR, self.setpointrR)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED + self.PIDrRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDfLeft.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)

    def follow_right(self):
        #print("fRight")

        self.PIDfRight.set_tunings(KP, KI, KD)
        self.PIDrRight.set_tunings(KP, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG
        self.setpointrL = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()
        self.inputrL = self._rleftIR.get_distance()              
            
        self.PIDfRight.compute(self.inputfR, self.setpointfR)
        self.PIDrLeft.compute(self.inputrL, self.setpointrL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDrLeft.output())/2, (MOTOR_SPEED + self.PIDfRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDrLeft.output())/2, -(MOTOR_SPEED + self.PIDfRight.output())/2)

    def follow_front_right(self):
        #print("ffRight")

        self.PIDfRight.set_tunings(KP2, KI, KD)
        self.setpointfR = WALL_DISTANCE_DIAG

        self.inputfR = self._frightIR.get_distance()

        self.PIDfRight.compute(self.inputfR, self.setpointfR)

        if self.dir:
            self.move_motors((MOTOR_SPEED - self.PIDfRight.output())/2, (MOTOR_SPEED + self.PIDfRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED - self.PIDfRight.output())/2, -(MOTOR_SPEED + self.PIDfRight.output())/2)

    def follow_front_left(self):
        #print("ffLeft")

        self.PIDfLeft.set_tunings(KP2, KI, KD)
        self.setpointfL = WALL_DISTANCE_DIAG

        self.inputfL = self._fleftIR.get_distance()

        self.PIDfLeft.compute(self.inputfL, self.setpointfL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDfLeft.output())/2, (MOTOR_SPEED - self.PIDfLeft.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDfLeft.output())/2, -(MOTOR_SPEED - self.PIDfLeft.output())/2)

    def follow_rear_right(self):
        #print("frRight")

        self.PIDrRight.set_tunings(KP2, KI, KD)
        self.setpointrR = WALL_DISTANCE_DIAG

        self.inputrR = self._rrightIR.get_distance()

        self.PIDrRight.compute(self.inputrR, self.setpointrR)

        if self.dir:
            self.move_motors((MOTOR_SPEED - self.PIDrRight.output())/2, (MOTOR_SPEED + self.PIDrRight.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED - self.PIDrRight.output())/2, -(MOTOR_SPEED + self.PIDrRight.output())/2)

    def follow_rear_left(self):
        #print("frLeft")

        self.PIDrLeft.set_tunings(KP2, KI, KD)
        self.setpointrL = WALL_DISTANCE_DIAG

        self.inputrL = self._rleftIR.get_distance()

        self.PIDrLeft.compute(self.inputrL, self.setpointrL)

        if self.dir:
            self.move_motors((MOTOR_SPEED + self.PIDrLeft.output())/2, (MOTOR_SPEED - self.PIDrLeft.output())/2)
        else:
            self.move_motors(-(MOTOR_SPEED + self.PIDrLeft.output())/2, -(MOTOR_SPEED - self.PIDrLeft.output())/2)


    def straight(self):
        #print("straight")
        if self.dir:
            self.move_motors(MOTOR_SPEED/2, MOTOR_SPEED/2)
        else:
            self.move_motors(-MOTOR_SPEED/2, -MOTOR_SPEED/2)
