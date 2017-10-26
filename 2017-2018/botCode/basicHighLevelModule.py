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
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        self.grid = copy.deepcopy(grid)

    def _get_direction(self, p_loc, next_loc):
        if p_loc[0] == next_loc[0]:
            if p_loc[1] < next_loc[1]:
                return PacmanCommand.NORTH
            else:
                return PacmanCommand.SOUTH
        else:
            if p_loc[0] < next_loc[0]:
                return PacmanCommand.EAST
            else:
                return PacmanCommand.WEST


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            p_loc = (self.state.pacman.x, self.state.pacman.y)
            
            # update game state
            if self.grid[p_loc[0]][p_loc[1]] in [o, O]:
                self.grid[p_loc[0]][p_loc[1]] = e
 
            path = bfs(self.grid, p_loc, self.state, [o, O])
            print(path)

            if path != None:
                next_loc = path[1]
                # Figure out position we need to move
                new_msg = PacmanCommand()
                new_msg.dir = self._get_direction(p_loc, next_loc)
                self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
                return

        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.STOP
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)


def main():
    module = BasicHighLevelModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
