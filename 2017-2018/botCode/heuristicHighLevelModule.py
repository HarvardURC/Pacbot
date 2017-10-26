#!/usr/bin/env python3

import os, copy
import robomodules as rm
from operator import itemgetter
from variables import *
from grid import grid
from search import bfs
from messages import MsgType, message_buffers, LightState, PacmanCommand

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60
PELLET_WEIGHT = 0.75
GHOST_WEIGHT = 0.25
GHOST_CUTOFF = 6

class HeuristicHighLevelModule(rm.ProtoModule):
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

    def _find_distance_of_closest_ghost(self, target_loc):
        dists = []
        for ghost in [self.state.red_ghost, self.state.pink_ghost, self.state.orange_ghost, self.state.blue_ghost]:
            # TODO: Use A* instead of manhattan
            dists.append(abs(ghost.x - target_loc[0]) + abs(ghost.y - target_loc[1]))
        return min(dists)

    def _find_distance_of_closest_pellet(self, target_loc):
         return len(bfs(self.grid, target_loc, self.state, [o])) - 1

    def _target_is_invalid(self, target_loc):
        return self.grid[target_loc[0]][target_loc[1]] in [I, n]

    def _find_best_target(self, p_loc):
        targets = [p_loc, (p_loc[0] - 1, p_loc[1]), (p_loc[0] + 1, p_loc[1]), (p_loc[0], p_loc[1] - 1), (p_loc[0], p_loc[1] + 1)]
        heuristics = []
        for target_loc in targets:
            if self._target_is_invalid(target_loc):
                heuristics.append(float('inf'))
                continue
            dist_to_pellet = self._find_distance_of_closest_pellet(target_loc)
            dist_to_ghost = self._find_distance_of_closest_ghost(target_loc)
            ghost_heuristic = 0 if dist_to_ghost > GHOST_CUTOFF else pow((GHOST_CUTOFF - dist_to_ghost), 2) * GHOST_WEIGHT
            pellet_heuristic = dist_to_pellet * PELLET_WEIGHT
            heuristics.append(ghost_heuristic + pellet_heuristic)
        print(heuristics)
        return targets[min(enumerate(heuristics), key=itemgetter(1))[0]]

    def _update_game_state(self):
        p_loc = (self.state.pacman.x, self.state.pacman.y)
        if self.grid[p_loc[0]][p_loc[1]] in [o, O]:
            self.grid[p_loc[0]][p_loc[1]] = e

    def _send_command_message_to_target(self, p_loc, target):
        new_msg = PacmanCommand()
        new_msg.dir = self._get_direction(p_loc, target)
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)

    def _send_stop_command(self):
        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.STOP
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
 
    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            self._update_game_state()
            p_loc = (self.state.pacman.x, self.state.pacman.y)
            next_loc = self._find_best_target(p_loc)
            if next_loc != p_loc:
                self._send_command_message_to_target(p_loc, next_loc)
                return
        self._send_stop_command()

        
def main():
    module = HeuristicHighLevelModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
