import sys, os
from variables import *
import pacmanState_pb2
from google.protobuf import message as proto_message
import time, struct, socket

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11297)
MAGIC_HEADER = 11297
SIZE_HEADER = struct.Struct("!HH")

def parse_game_mode(mode):
    if mode == pacmanState_pb2.PacmanState.FRIGHTENED:
        return 'frightened'
    elif mode == pacmanState_pb2.PacmanState.CHASE:
        return 'chase'
    elif mode == pacmanState_pb2.PacmanState.SCATTER:
        return 'scatter'
    else:
        return 'undefined'

def clear_rows(rows_count):
    for row in range(rows_count):
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K")

def display_game(state):
    clear_rows(100)
    mode = parse_game_mode(state.mode)
    print("Pacman  Score: " + str(state.score) + "  State: " + str(mode) + "  Lives: " + str(state.lives))
    displayBuf = []
    row_index = 0
    col_index = 0
    cur_row = []
    for el in enumerate(state.grid):
        if (row_index,col_index) == (state.pacman.x, state.pacman.y):
            cur_row.append('P')
        elif (row_index,col_index) == (state.red_ghost.x, state.red_ghost.y) or (row_index,col_index) == (state.orange_ghost.x, state.orange_ghost.y) or (row_index,col_index) == (state.pink_ghost.x, state.pink_ghost.y) or (row_index,col_index) == (state.blue_ghost.x, state.blue_ghost.y):
            cur_row.append('G')
        elif el == pacmanState_pb2.PacmanState.PELLET:
            cur_row.append('.')
        elif el == pacmanState_pb2.PacmanState.POWER_PELLET:
            cur_row.append('o')
        elif el == pacmanState_pb2.PacmanState.EMPTY:
            cur_row.append(' ')
        elif el == pacmanState_pb2.PacmanState.WALL:
            cur_row.append('0')
        col_index += 1
        if col_index >= state.grid_columns:
            col_index = 0
            row_index += 1
            displayBuf.append(cur_row)
            cur_row = []
    inverted = zip(*displayBuf)
    for row in reversed(list(inverted)):
        for el in row:
            print(el, end='')
        print()

class FancySocket:
    def __init__(self, addr=ADDRESS, port=PORT):
        self.addr = addr
        self.port = port

    def connect(self):
        self.s = socket.socket()
        self.s.connect((self.addr, self.port))
        self.s.setblocking(False)

    def __read_data(self, size):
        data = b""
        while len(data) < size:
            try:
                data += self.s.recv(size - len(data))
            except BlockingIOError:
                time.sleep(0.05)
        return data
        
    def read_msg(self):
        """
        Read a message from the socket and return it.
        This function is allowed to return None if it cannot read a message.

        This function is currently blocking, i.e. it will not return until
        it has read a message or reached an error condition.

        It is important to call this function often, otherwise messages may
        overflow the socket's buffer.

        Currently, the biggest downside of this implmentation is that it does
        not detect if the connection is dropped, it just waits forever.
        """
        magic, length = SIZE_HEADER.unpack(self.__read_data(SIZE_HEADER.size))
        if magic != MAGIC_HEADER:
            # Uh oh, what happened?
            self.s.close()
            print("Magic number mismatched, reconnecting...",
                  file=sys.stderr)
            self.connect()
            return
        msg = pacmanState_pb2.PacmanState()
        try:
            msg.ParseFromString(self.__read_data(length))
            return msg
        except proto_message.Error:
            return

    # Whee, context managers
    __enter__ = connect
    def __exit__(self, *args):
        self.s.close()

def main():
    s = FancySocket()
    with s:
        while True:
            msg = s.read_msg()
            if msg:
                display_game(msg)
            time.sleep(1.0/10)

if __name__ == "__main__":
    main()
