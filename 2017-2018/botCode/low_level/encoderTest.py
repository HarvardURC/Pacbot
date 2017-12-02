import encoders
from pins import *
from GPIOhelpers import *
from time import sleep

def main():
    encoder = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
    position = -999
    while(True):
        new_pos = encoder.read()
        if new_pos != position:
            print("Position = %f", new_pos)
            position = new_pos
            
        sleep(1)

main()
