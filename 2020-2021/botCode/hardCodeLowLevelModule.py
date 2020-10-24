#!/usr/bin/env python3

import os
import robomodules as rm
import variables as var
from grid import grid
from low_level.motors import Motors
from messages import MsgType, message_buffers, LightState, PacmanCommand
from time import sleep
ADDRESS = os.environ.get("LOCAL_ADDRESS","192.168.0.100")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 10

GRID_VAL = 200

class LowLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.cmd_idx = 0
        self.state = PAUSED
        self.commands = [
               'forward 7',
               'tr',
               'forward 3',
               'tl',
               'forward 3',
               'tl',
               'forward 3',
               'tr',
               'forward 2',
               'tl',
               'forward 3',
               'tl',
               'forward 11',
               'tl',
               'forward 3',
               'tr',
               'forward 9',
               'tl',
               'forward 3',
               'tr',
               'forward 3',
               'tr',
               'forward 3',
               'tl',
               'forward 2',
               'tr',
               'forward 3',
               'tr',
               'forward 11',
               'tr',
               'forward 3',
               'tr',
               'forward 3',
               'tl',
               'forward 3',
               'tl',
               'forward 3',
               'tr',
               'forward 3',
               'tl',
               'forward 14',
               'tl',
               'forward 3',
               'tl',
               'forward 5',
               'tr',
               'forward 18',
               'tr',
               'forward 5',
               'tl',
               'forward 7',
               'tl',
               'forward 11',
               'tl',
               'forward 4,'
               'tr',
               'forward 14',
               'tr',
               'forward 4',
               'tr',
               'forward 5',
               'tr',
               'forward 25',
               'tr',
               'forward 5',
               'tl',
               'forward 3',
               'tl',
               'forward 14',
               'tl',
               'forward 3',
               'tr',
               'forward 3',
               'tl',
               'forward 3',
               'tr',
               'forward 3',
               'tl']
        self.motors = Motors()
        print('ready')
        
    def _move_forward(self, cells):
        self.motors.move_cells(cells)

    def _turn_right(self):
        self.motors.turn_right()
            
    def _turn_left(self):
        self.motors.turn_left()

    def _reverse(self, ticks):
        self.motors.reverse_direction()
        self._turn_around()
        self._move_forward(ticks)

    def _execute_command(self):
        if self.state == 1:
            print(self.cmd_idx)
            return
        cmd = self.commands[self.cmd_idx]
        self.cmd_idx += 1
        if cmd == 'tl':
            self.turn_left()
        elif cmd == 'tr':
            self.turn_right()
        elif 'forward' in cmd:
            self._move_forward(cmd.split()[1])
        elif 'rev' in cmd:
            self._reverse(cmd.split()[1])
                
    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg.mode

    def tick(self):
        self.set_frequency(0)
        self._execute_command()
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
