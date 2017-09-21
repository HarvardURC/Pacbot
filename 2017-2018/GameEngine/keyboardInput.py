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
SPEED = 1.0

class InputClient:
    def __init__(self, loop):
        self.loop = loop
        coro = asyncio.open_connection(ADDRESS, INPUT_PORT, loop=loop)
        self.read_client = AsyncClient(ADDRESS, BIND_PORT, self._update_state, loop)
        _, self.writer = loop.run_until_complete(coro)
        self.loop.add_reader(sys.stdin, self.keypress)
        self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.cur_dir = right
        self.next_dir = right
        self.state = PacmanState()
        self.state.mode = PacmanState.PAUSED
        self.lives = starting_lives
        self.clicks = 0
        self.loop.call_later(1/(SPEED*game_frequency), self.game_tick)

    def _update_state(self, msg):
        self.state = msg
        if self.state.lives != self.lives:
            self.lives = self.state.lives
            self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]

    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            self.pacbot_pos[0] += 1
            self.cur_dir = direction
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            self.pacbot_pos[0] -= 1
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            self.pacbot_pos[1] += 1
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            self.pacbot_pos[1] -= 1
            self.cur_dir = direction
            return True
        return False

    def run(self):
        try:
            with self.read_client:
                self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        self.writer.close()
        self.loop.stop()

    def write(self, msg):
        self.writer.write(pack_msg(msg))

    def game_tick(self):
        if self.state.mode != PacmanState.PAUSED:
            if not self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1]):
                self._move_if_valid_dir(self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])
        pos_buf = PacmanState.AgentState()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString())
        self.loop.call_later(1/(SPEED*game_frequency), self.game_tick)

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
