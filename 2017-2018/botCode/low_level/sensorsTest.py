from pins import *
from sensors import Sensors
from time import sleep

sensors = Sensors([pins.tof_left, pins.tof_right], ["left", "right"], [0x29, 0x29])
while True:
    sensors.print_all_values()
    sleep(1)
