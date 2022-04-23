#!/usr/bin/env python3

import os
import robomodules as rm
import variables as var
from grid import grid
from low_level.motors import Motors
from low_level.motors import Direction
from messages import MsgType, message_buffers, LightState, PacmanCommand
from time import sleep
ADDRESS = os.environ.get("LOCAL_ADDRESS","192.168.0.101")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 100 # was 10

GRID_VAL = 200

class LowLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND, MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.current_command = None
        self.current_location = None
        self.motors = Motors()

        print('ready')
        self.prev_loc = None
        self.ticks = 0
        self.forwards = 0
        

    def _move_forward(self):
        self.motors.move_cells(1)

    def _execute_command(self):
        if self.current_command:
            #print(self.current_dir)
            cmd = self.current_command
            self.current_command = None

            if cmd == PacmanCommand.STOP:
                self.kill()
                return
            
            if cmd == PacmanCommand.NORTH:
                motor_dir = Direction.N
            elif cmd == PacmanCommand.SOUTH:
                motor_dir = Direction.S
            elif cmd == PacmanCommand.WEST:
                motor_dir = Direction.W
            else:
                motor_dir = Direction.E
            
            self.motors.drive_in_direction(motor_dir, 1)

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PACMAN_COMMAND:
            self.current_command = msg.dir
        elif msg_type == MsgType.LIGHT_STATE:
            if self.ticks % 5 == 0:
                self.current_location = (msg.pacman.x, msg.pacman.y)
            self.ticks += 1

    def tick(self):
        self.set_frequency(0)
        if self.current_command:
            self._execute_command()
        #else:
        #self.kill()
        self.loop.call_soon(self.tick)

    def kill(self):
        self.motors.stop()


def main():
    module = LowLevelModule(ADDRESS, PORT)
    try:
        module.run()
    except KeyboardInterrupt:
        module.kill()
if __name__ == "__main__":
    main()
