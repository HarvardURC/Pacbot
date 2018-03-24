from pins import *
from sensors import Sensors
from time import sleep

sensors = Sensors([pins.tof_fleft,pins.tof_front,pins.tof_fright,pins.tof_rear, pins.tof_rright, pins.tof_rleft], ["fleft", "front","fright","rear","rleft","rright"], [0x30,0x31,0x32,0x33,0x34])
while True:
    sensors.print_all_values()
    sleep(1)
