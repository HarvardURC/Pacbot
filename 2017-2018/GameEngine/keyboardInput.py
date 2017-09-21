#!/usr/bin/env python3

import asyncio, sys, os, curses

from comm import pack_msg
from comm.pacmanState_pb2 import PacmanState
from comm.asyncclient import AsyncClient
from pacbot.variables import *
from pacbot.grid import *

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
INPUT_PORT = os.environ.get("INPUT_PORT", 11295)
BIND_PORT = os.environ.get("BIND_PORT", 11297)

class InputClient:
    def __init__(self, loop):
        self.loop = loop
        coro = asyncio.open_connection(ADDRESS, INPUT_PORT, loop=loop)
        self.readClient = AsyncClient(ADDRESS, BIND_PORT, self._update_state, loop)
        _, self.writer = loop.run_until_complete(coro)
        self.loop.add_reader(sys.stdin, self.keypress)
        self.pacbot_pos = [pacbot_starting_pos[0]*1.0, pacbot_starting_pos[1]*1.0]
        self.cur_dir = right
        self.next_dir = right
        self.state = PacmanState()
        self.state.mode = PacmanState.PAUSED
        self.loop.call_later(1/(5*game_frequency), self.game_tick)
        with self.readClient:
            loop.run_forever()

    def _update_state(self, msg):
        self.state = msg

    def _move_if_valid_dir(self, direction, round_x, round_y):
        if direction == right and grid[round_x + 1][round_y] not in [I, n]:
            self.pacbot_pos[0] += 1.0/5
            self.cur_dir = direction
            return True
        elif direction == left and grid[round_x - 1][round_y] not in [I, n]:
            self.pacbot_pos[0] -= 1.0/5
            self.cur_dir = direction
            return True
        elif direction == up and grid[round_x][round_y + 1] not in [I, n]:
            self.pacbot_pos[1] += 1.0/5
            self.cur_dir = direction
            return True
        elif direction == down and grid[round_x][round_y - 1] not in [I, n]:
            self.pacbot_pos[1] -= 1.0/5
            self.cur_dir = direction
            return True
        return False

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        self.writer.close()
        self.loop.stop()

    def write(self, msg):
        self.writer.write(pack_msg(msg))

    def game_tick(self):
        round_x = round(self.pacbot_pos[0])
        round_y = round(self.pacbot_pos[1])
        if self.state.mode != PacmanState.PAUSED:
            if not self._move_if_valid_dir(self.next_dir, round_x, round_y):
                self._move_if_valid_dir(self.cur_dir, round_x, round_y)

        pos_buf = PacmanState.Position()
        pos_buf.x = round(self.pacbot_pos[0])
        pos_buf.y = round(self.pacbot_pos[1])
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString())
        self.loop.call_later(1/(5*game_frequency), self.game_tick)

    def keypress(self):
        char = sys.stdin.read(1)
        if char == 'a':
            self.next_dir = left
        elif char == 'd':
            self.next_dir = right
        elif char == 'w':
            self.next_dir = up
        elif char == 's':
            self.next_dir = down
        elif char == 'q':
            self.quit()

def main():
    loop = asyncio.get_event_loop()
    client = InputClient(loop)
    curses.wrapper(lambda scr: client.run())

if __name__ == "__main__":
    main()
