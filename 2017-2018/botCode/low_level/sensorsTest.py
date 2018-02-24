from pins import *
from sensors import Sensors
from time import sleep

sensors = Sensors([pins.tof_fleft, pins.tof_fright], ["left", "right"], [0x29, 0x30])
while True:
    sensors.print_all_values()
    sleep(1)
