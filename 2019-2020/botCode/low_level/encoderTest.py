from encoders import Encoder
from pins import *
from GPIOhelpers import *
from time import sleep

def main():
    encoder_r = Encoder(pins.encoder_pin_r1, pins.encoder_pin_r2)
    position_r = -999
    encoder_l = Encoder(pins.encoder_pin_l1, pins.encoder_pin_l2)
    position_l = -999
    while(True):
        new_pos_r = -encoder_r.read()
        new_pos_l = encoder_l.read()
        if new_pos_r != position_r or new_pos_l != position_l:
            print("Position_r = {}".format(new_pos_r))
            position_r = new_pos_r
            print("Position_l = {}".format(new_pos_l))
            postion_l = new_pos_l
            
        sleep(1)
main()
