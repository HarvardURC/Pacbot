from time import sleep
from .GPIOhelpers import *
#from GPIOhelpers import *
import pigpio
setGPIO()

class Encoder:
    def __init__(self, pin_a, pin_b):
        pi = pigpio.pi()
        self._pin_a = pin_a
        self._pin_b = pin_b
        self._position = 0

        pi.set_mode(self._pin_a, pigpio.INPUT)
        pi.set_mode(self._pin_b, pigpio.INPUT)
        # digitalMode(self._pin_a, INPUT)
        # digitalMode(self._pin_b, INPUT)

        cb1 = pi.callback(self._pin_a, pigpio.EITHER_EDGE, self._interrupt_a)
        cb2 = pi.callback(self._pin_b,  pigpio.EITHER_EDGE, self._interrupt_b)
        # attachInterrupt(self._pin_a, self._interrupt_a, CHANGE);
        # attachInterrupt(self._pin_b, self._interrupt_b, CHANGE);

    def _interrupt_a(self, gpio, level, tick):
        if (pi.read(self._pin_a) == 1):
            if (pi.read(self._pin_b) == 0):
                self._position += 1
            else:
                self._position -= 1

        else:
            if (pi.read(self._pin_b) == 0):
                self._position -= 1
            else:
                self._position += 1

    def _interrupt_b(self, gpio, level, tick):
        if (pi.read(self._pin_b) == 1):
            if (pi.read(self._pin_a) == 1):
                self._position += 1
            else:
                self._position -= 1

        else:
            if (pi.read(self._pin_a) == 0):
                self._position += 1
            else:
                self._position -= 1

    def read(self):
        return self._position

    def reset(self):
        self._position = 0

    def write(self, pos):
        self._position = pos
