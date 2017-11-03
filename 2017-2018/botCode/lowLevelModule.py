#!/usr/bin/env python3

import os
import robomodules as rm
import variables as var
from grid import grid
from sensor import DistSensor
from messages import MsgType, message_buffers, LightState, PacmanCommand

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60

class LowLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND, MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.current_command = None
        self.current_location = None
        self.current_dir = PacmanCommand.EAST
        self.sensors = [DistSensor(i) for i in range(1, 8)]
        
    def _should_move_forward(self, cur_dir, cmd):
        return cur_dir == cmd

    def _move_forward(self):
        #TODO: move forward one unit

    def _execute_command(self):
        if self.current_command:
            cmd = self.current_command
            self.current_command = None
            if self._should_move_forward():
                self._move_forward()
            else:
                #TODO: other cases
                # example for getting sensor reading
                self.sensors[7].get_reading()

        self._execute_command()

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PACMAN_COMMAND:
            self.current_command = msg.dir
        elif msg_type == MsgType.LIGHT_STATE:
            self.current_location = (msg.pacman.x, msg.pacman.y)

    def tick(self):
        if self.current_command:
            self.set_frequency(0)
            self._execute_command()


def main():
    module = LowLevelModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
