#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
from time import sleep

port_list = ["/dev/ttyAMA0","/dev/serial1","/dev/ttyS0","/dev/serial0"]
#port_list = ["/dev/ttyAMA0"]
for port in port_list:
    serialPort = serial.Serial(port, 38400, timeout = 2)
    #serialPort.write(b'a')
    #while 1:
    print(serialPort.read(2))
    #serialPort.reset_input_buffer()
    serialPort.close()
