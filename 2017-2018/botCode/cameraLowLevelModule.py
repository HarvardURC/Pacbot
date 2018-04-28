#!/usr/bin/env python3

import os
import robomodules as rm
import variables as var
from grid import grid
from low_level.motors import Motors
from messages import MsgType, message_buffers, LightState, PacmanCommand
from time import sleep
ADDRESS = os.environ.get("LOCAL_ADDRESS","192.168.0.101")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 10

GRID_VAL = 200

class LowLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND, MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.current_command = None
        self.current_location = None
        self.motors = Motors()
        self.current_dir = PacmanCommand.EAST
        print('ready')
        self.prev_loc = None
        self.ticks = 0
        self.forwards = 0
        
    def _should_turn_left(self, cmd):
        return \
            (self.current_dir == PacmanCommand.NORTH and cmd  == PacmanCommand.WEST) or \
            (self.current_dir == PacmanCommand.SOUTH and cmd  == PacmanCommand.EAST) or \
            (self.current_dir == PacmanCommand.EAST and cmd  == PacmanCommand.NORTH) or \
            (self.current_dir == PacmanCommand.WEST and cmd  == PacmanCommand.SOUTH)

    def _should_turn_right(self, cmd):
        return \
            (self.current_dir == PacmanCommand.NORTH and cmd  == PacmanCommand.EAST) or \
            (self.current_dir == PacmanCommand.SOUTH and cmd  == PacmanCommand.WEST) or \
            (self.current_dir == PacmanCommand.EAST and cmd  == PacmanCommand.SOUTH) or \
            (self.current_dir == PacmanCommand.WEST and cmd  == PacmanCommand.NORTH)

    def _should_reverse(self, cmd):
        return \
            (self.current_dir == PacmanCommand.NORTH and cmd  == PacmanCommand.SOUTH) or \
            (self.current_dir == PacmanCommand.SOUTH and cmd  == PacmanCommand.NORTH) or \
            (self.current_dir == PacmanCommand.EAST and cmd  == PacmanCommand.WEST) or \
            (self.current_dir == PacmanCommand.WEST and cmd  == PacmanCommand.EAST)

    def _move_forward(self):
        self.motors.move_cells(1)

    def _turn_right(self):
        self.motors.turn_right()
        if self.current_dir == PacmanCommand.EAST:
            self.current_dir = PacmanCommand.SOUTH
        elif self.current_dir == PacmanCommand.SOUTH:
            self.current_dir = PacmanCommand.WEST
        elif self.current_dir == PacmanCommand.WEST:
            self.current_dir = PacmanCommand.NORTH
        else:
            self.current_dir = PacmanCommand.EAST
            
    def _turn_left(self):
        self.motors.turn_left()
        if self.current_dir == PacmanCommand.EAST:
            self.current_dir = PacmanCommand.NORTH
        elif self.current_dir == PacmanCommand.NORTH:
            self.current_dir = PacmanCommand.WEST
        elif self.current_dir == PacmanCommand.WEST:
            self.current_dir = PacmanCommand.SOUTH
        else:
            self.current_dir = PacmanCommand.EAST

    def _turn_around(self):
        #TODO: Turn 180 degrees
        if self.current_dir == PacmanCommand.EAST:
            self.current_dir = PacmanCommand.WEST
        elif self.current_dir == PacmanCommand.NORTH:
            self.current_dir = PacmanCommand.SOUTH
        elif self.current_dir == PacmanCommand.WEST:
            self.current_dir = PacmanCommand.EAST
        else:
            self.current_dir = PacmanCommand.NORTH
    
    def _reverse(self):
        #print("reverse")
        self.motors.reverse_direction()
        self._turn_around()
        self._move_forward()

    def _execute_command(self):
        if self.current_command:
            #print(self.current_dir)
            cmd = self.current_command
            self.current_command = None
            if cmd == PacmanCommand.STOP:
                self.motors.stop()
                return
            if self._should_turn_left(cmd):
                print("tl")
                self._turn_left()
                self.forwards = 0
                #self.motors.move_cells(1)
                #self.loc = self.current_location
            elif self._should_turn_right(cmd):
                print("tr")
                self._turn_right()
                self.forwards = 0
                #self.motors.move_cells(1)
                #loc = self.current_location
            if self._should_reverse(cmd):
                print("r")
                """
                self.forwards = 0
                self.motors.turn_around_l()
                self.motors.move_cells(1)
                self._turn_around()
 
                if self.prev_loc != self.current_location:
                        self.forwards = 0
            
                self.prev_loc = self.current_location 
                self._reverse()
                self.forwards +=1
            
            
                self.motors.turn_around_l()
                self.motors.move_cells(1)
                self._turn_around()
                """
                self.motors.reverse_direction()
                self.motors.move_cells(1)
                self.motors.reverse_direction()
                self.forwards = 0

                                               
            else:
                if self.prev_loc == self.current_location and self.forwards > 1:
                    self.motors.escape()
                    self.forwards = 0
                
                else:
                    print("f")
                    if self.prev_loc != self.current_location:
                        self.forwards = 0
                    self.prev_loc = self.current_location
                    self._move_forward()
                    self.forwards += 1
                
    def _set_direction(self, prev_loc):
        if prev_loc[0] > self.current_location[0]:
            self.current_dir = PacmanCommand.WEST
        elif prev_loc[0] < self.current_location[0]:
            self.current_dir = PacmanCommand.EAST
        elif prev_loc[1]> self.current_location[1]:
            self.current_dir = PacmanCommand.SOUTH
        elif prev_loc[1] < self.current_location[1]:
            self.current_dir = PacmanCommand.NORTH

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PACMAN_COMMAND:
            self.current_command = msg.dir
        elif msg_type == MsgType.LIGHT_STATE:
            if self.ticks % 5 != 0:
                self.ticks += 1
                return
            prev_loc = self.current_location
            self.current_location = (msg.pacman.x, msg.pacman.y)
            if prev_loc != None:
                self._set_direction(prev_loc)
            self.ticks += 1

    def tick(self):
        self.set_frequency(0)
        if self.current_command:
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
