#!/usr/bin/env python3

import os, copy
import robomodules as rm
from variables import *
from grid import grid
from search import bfs
from messages import MsgType, message_buffers, LightState, PacmanCommand

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60

class BasicHighLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.next_dir = None

    def msg_received(self, msg, msg_type):
        return

    def tick(self):
        if self.next_dir == None:
            self.keypress()
        else:
            new_msg = PacmanCommand()
            new_msg.dir = self.next_dir
            self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
            self.next_dir = None

    def keypress(self):
        char = input('direction: ')
        if char == 'a':
            self.next_dir = PacmanCommand.WEST
        elif char == 'd':
            self.next_dir = PacmanCommand.EAST
        elif char == 'w':
            self.next_dir = PacmanCommand.NORTH
        elif char == 's':
            self.next_dir = PacmanCommand.SOUTH
        elif char == 'q':
            self.quit()

def main():
    module = BasicHighLevelModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
