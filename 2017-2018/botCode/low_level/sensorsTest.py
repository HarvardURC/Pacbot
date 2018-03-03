from pins import *
from sensors import Sensors
from time import sleep

sensors = Sensors([pins.tof_fleft,pins.tof_front,pins.tof_fright], ["left", "front","right"], [0x30,0x31,0x32])
while True:
    sensors.print_all_values()
    sleep(1)
