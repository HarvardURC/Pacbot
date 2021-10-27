#!/usr/bin/env python3

import sys, os, time
import robomodules as rm
#from serial import Serial
import serial.tools.list_ports
import serial
from xbee import ZigBee
from messages import *

ADDRESS = os.environ.get("SERVER_ADDRESS","192.168.0.100")
PORT = os.environ.get("SERVER_PORT", 11297)

FREQUENCY = 10

class XbeeModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        ports = list(serial.tools.list_ports.comports())
        dev = None
        for p in ports:
            print(p[1])
            if 'FT' in p[1]:
                dev = p[0]
        self.xbee = serial.Serial(dev, 9600)


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.FULL_STATE:
            self.state = msg

    def tick(self):
        if self.state:
            if self.state.mode == PacmanState.PAUSED:
                mode = 'P'
            else:
                mode = 'R'
            m = '${}#{}#{}'.format(mode, self.state.score, self.state.lives)
            m += '#{}#{}'.format(self.state.pacman.x, self.state.pacman.y)
            g_state = 'F' if self.state.red_ghost.frightened_counter > 0 else 'N'
            m += '#{}#{}#{}'.format(self.state.red_ghost.x, self.state.red_ghost.y, g_state)
            g_state = 'F' if self.state.pink_ghost.frightened_counter > 0 else 'N'
            m += '#{}#{}#{}'.format(self.state.pink_ghost.x, self.state.pink_ghost.y, g_state)
            g_state = 'F' if self.state.orange_ghost.frightened_counter > 0 else 'N'
            m += '#{}#{}#{}'.format(self.state.orange_ghost.x, self.state.orange_ghost.y, g_state)
            g_state = 'F' if self.state.blue_ghost.frightened_counter > 0 else 'N'
            m += '#{}#{}#{}%\n'.format(self.state.blue_ghost.x, self.state.blue_ghost.y, g_state)
            self.xbee.write(m.encode())
            print(m.encode())
            print('wrote')


def main():
    module = XbeeModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
