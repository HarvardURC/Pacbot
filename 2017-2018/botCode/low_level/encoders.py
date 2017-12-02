from time import sleep
from GPIOhelpers import *

class Encoder:
    def __init__(self, pin_a, pin_b):
        self._pin_a = pin_a
        self._pin_b = pin_b
        self._position = 0

        digitalMode(self._pin_a, INPUT_PULLUP)
        digitalMode(self._pin_b, INPUT_PULLUP)

        sleep(2)

        attachInterrupt(self._pin_a, self._interrupt_a, CHANGE);
        attachInterrupt(self._pin_b, self._interrupt_b, CHANGE);

    def _interrupt_a(self):
      	if (digitalRead(self._pin_a) == HIGH):
            if (digitalRead(self._pin_b) == LOW):
                self._position += 1
            else:
                self._position -= 1

        else:
            if (digitalRead(self._pin_b) == LOW):
                self._position -= 1
            else:
                self._position += 1

    def _interrupt_b(self):
        if (digitalRead(self._pin_b) == HIGH):
            if (digitalRead(self._pin_a) == HIGH):
                self._position += 1
            else:
                self._position -= 1

        else:
            if (digitalRead(self._pin_a) == LOW):
                self._position += 1
            else:
                self._position -= 1

    def read(self):
        return self._position

    def write(self, pos):
        self._position = pos
