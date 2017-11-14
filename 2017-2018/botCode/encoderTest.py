import encoders
from pins import *
from GPIOhelpers import *
from time import sleep

encoder = Encoder(pins.encoderPinL1, pins.encoderPinL2)

position = -999

def main():
	while(True):
		newPos = encoder.read()
		if newPos != position:
			print("Position = %f", newPos)
			position = newPos

		# if sys.stdin.readlines() != None:
		# 	print("Encoder reset to zero")
		# 	encoder.write(0)

		sleep(1)


