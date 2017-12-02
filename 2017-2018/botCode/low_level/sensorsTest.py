from pins import *
from sensors import Sensors
from time import sleep

sensors = Sensors([pins.tof_left, pins.tof_right], ["left", "right"])
while True:
    sensors.print_all_values()
    sleep(10)
