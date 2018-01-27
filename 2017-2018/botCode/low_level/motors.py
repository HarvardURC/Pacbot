from motor import *
from encoders import Encoder
from pins import *
from sensors import Sensors


setGPIO()



class Motors:
    def __init__(self, leftIR, leftDiagIR, frontIR, rightDiagIR, rightIR):
        self._frontIR = frontIR
        self._leftIR = leftIR
        self._rightIR = rightIR
        self._leftDiagIR = leftDiagIR
        self._rightDiagIR = rightDiagIR

        self.encoderLeft = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
        self.encoderRight = Encoder(pins.encoder_pin_r1, pins.encoder_pin_r2)

        self.left_motor = Motor("Left", pins.motor_power_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_power_r, pins.motor_direction_r, 0)

    def forward():
        self.advance()
        self.move_ticks(,)

    def turn_around_l():
        self.turn_left()
        self.turn_left()

    def turn_around_r():
        self.turn_right()
        self.turn_right()

    def turn_left():
        if self._frontIR.get_distance() < WALL_THRESHOLD:
            self.front_align()
        self.move_ticks(-1 * TICKS_TURN, TICKS_TURN)

    def turn_right():
        if self._frontIR.get_distance() < WALL_THRESHOLD:
            self.front_align()
        self.move_ticks(TICKS_TURN, -1 * TICKS_TURN)
