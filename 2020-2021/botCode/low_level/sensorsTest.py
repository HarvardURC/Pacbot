from pins import *
from sensors import Sensors
from time import sleep

#sensors = Sensors([pins.tof_fleft,pins.tof_fright], ["fleft","fright"], [0x32,0x33])
sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright,pins.tof_rleft,pins.tof_rright], ["front", "rear","fleft","fright","rleft","rright"], [0x30,0x31,0x32,0x33,0x34,0x35])

while True:
    sensors.print_all_values()
    print()
    sleep(1)
