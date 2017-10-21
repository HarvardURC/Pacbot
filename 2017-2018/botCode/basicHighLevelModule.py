#!/usr/bin/env python3

import os, copy
import robomodules as rm
import variables as var
from .grid import grid
from .search import bfs
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

    def _get_direction(self, pac_loc, next_loc):
        if pac_loc.x == next_loc[0]:
            if pac_loc.y < next_loc[1]:
                return PacmanCommand.Direction.NORTH
            else:
                return PacmanCommand.Direction.SOUTH
        else:
            if pac_loc.x < next_loc[0]:
                return PacmanCommand.Direction.EAST
            else:
                return PacmanCommand.Direction.WEST


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        if self.state and self.state.mode == LightState.GameMode.RUNNING:

            # update game state
            if self.grid[self.state.pacman.x][self.state.pacman.y] in [o, O]:
                self.grid[self.state.pacman.x][self.state.pacman.y] = e

            path = bfs(self.grid, self.state, [o, O])

            if path != None:
                next_loc = path[1]
                # Figure out position we need to move
                new_msg = PacmanCommand()
                new_msg.dir = self._get_direction(self.state.pacman, next_loc)
                self.write(new_msg.SerializeToString, PACMAN_COMMAND)
                return

        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.Direction.STOP
        self.write(new_msg.SerializeToString(), PACMAN_COMMAND)


def main():
    module = BasicHighLevelModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
