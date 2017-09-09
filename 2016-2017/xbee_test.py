from serial import Serial
from xbee import XBee
import time
from threading import Thread, Lock

def xBee():
    xbee = Serial('/dev/cu.usbserial-DA00VDM1', 9600)
    # xbee = XBee(serial_port)
    # def send_state():
    #     xbee.tx(data="hello_world")
    while True:
        try:
            xbee.write("hello")
            # xbee.send("hello_world", command='MY')
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    xbee.halt
    serial_port.close()

Thread(target = xBee).start()
