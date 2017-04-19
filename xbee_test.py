import serial
from xbee import XBee
import time
from threading import Thread, Lock

def xBee():
    serial_port = serial.Serial('/dev/ttyUSB0', 9600)
    def send_state(data):
        xbee.tx(dest_addr='\x00\x01', data=pacBot())
    xbee = XBee(ser)
    while True:
        try:
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
    xbee.helt
    serial_port.close()

Thread(target = xBee).start()
