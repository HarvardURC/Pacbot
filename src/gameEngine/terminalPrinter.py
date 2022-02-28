#!/usr/bin/env python3

from __future__ import print_function

import sys, os, time
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

class TerminalPrinter(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None

    def _parse_game_mode(self, mode):
        if mode == PacmanState.FRIGHTENED:
            return 'frightened'
        elif mode == PacmanState.CHASE:
            return 'chase'
        elif mode == PacmanState.SCATTER:
            return 'scatter'
        else:
            return 'undefined'

    def _clear_rows(self, rows_count):
        for row in range(rows_count):
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K")

    def _display_game(self):
        if not self.state:
            return
        state = self.state
        self._clear_rows(100)
        mode = self._parse_game_mode(state.mode)
        print("Pacman  Score: " + str(state.score) + "  State: " + str(mode) + "  Lives: " + str(state.lives))
        displayBuf = []
        row_index = 0
        col_index = 0
        cur_row = []
        for el in state.grid:
            if (col_index, row_index) == (state.pacman.x, state.pacman.y):
                cur_row.append('P')
            elif (col_index, row_index) == (state.red_ghost.x, state.red_ghost.y) or (col_index, row_index) == (state.orange_ghost.x, state.orange_ghost.y) or (col_index, row_index) == (state.pink_ghost.x, state.pink_ghost.y) or (col_index, row_index) == (state.blue_ghost.x, state.blue_ghost.y):
                cur_row.append('G')
            elif el == PacmanState.PELLET:
                cur_row.append('.')
            elif el == PacmanState.POWER_PELLET:
                cur_row.append('o')
            elif el == PacmanState.EMPTY:
                cur_row.append(' ')
            elif el == PacmanState.WALL:
                cur_row.append('0')
            row_index += 1
            if row_index >= state.grid_columns:
                row_index = 0
                col_index += 1
                displayBuf.append(cur_row)
                cur_row = []
        inverted = zip(*displayBuf)
        for row in reversed(list(inverted)):
            for el in row:
                print(el, end='')
            print('')


    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.FULL_STATE:
            self.state = msg
        

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        self._display_game()

  
def main():
    printer = TerminalPrinter(ADDRESS, PORT)
    printer.run()

if __name__ == "__main__":
    main()
