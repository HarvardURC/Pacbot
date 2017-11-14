from time import sleep
from GPIOhelpers import *

class Encoder:
	def __init__(self, pinA, pinB):
		self._pinA = pinA
		self._pinB = pinB
		self._position = 0

		digitalMode(self._pinA, INPUT_PULLUP)
		digitalMode(self._pinB, INPUT_PULLUP)

		sleep(2)

		attachInterrupt(self._pinA, self._interruptA, CHANGE);
		attachInterrupt(self._pinB, self._interruptB, CHANGE);

	def _interruptA(self):
	  	if (digitalRead(self._pinA) == HIGH):
	    	if (digitalRead(self._pinB) == LOW):
	      		self._position += 1
	    	else:
	      		self._position -= 1
	   
	  	else:
	    	if (digitalRead(self._pinB) == LOW):
	      		self._position -= 1
	    	else:
	      		self._position += 1

	def _interruptB(self):
	  	if (digitalRead(self._pinB) == HIGH):
	    	if (digitalRead(self._pinA) == HIGH):
	      		self._position += 1
	    	else:
	      		self._position -= 1
	   
	  	else:
	    	if (digitalRead(self._pinA) == LOW):
	      		self._position += 1
	    	else:
	      		self._position -= 1

	def read(self):
		return self._position

	def write(self, pos):
		return self._position = pos

