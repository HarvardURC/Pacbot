import sys, os
import pacmanState_pb2
import time
from client import EngineClient

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11297)

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
    for el in state.grid:
        if (col_index, row_index) == (state.pacman.x, state.pacman.y):
            cur_row.append('P')
        elif (col_index, row_index) == (state.red_ghost.x, state.red_ghost.y) or (col_index, row_index) == (state.orange_ghost.x, state.orange_ghost.y) or (col_index, row_index) == (state.pink_ghost.x, state.pink_ghost.y) or (col_index, row_index) == (state.blue_ghost.x, state.blue_ghost.y):
            cur_row.append('G')
        elif el == pacmanState_pb2.PacmanState.PELLET:
            cur_row.append('.')
        elif el == pacmanState_pb2.PacmanState.POWER_PELLET:
            cur_row.append('o')
        elif el == pacmanState_pb2.PacmanState.EMPTY:
            cur_row.append(' ')
        elif el == pacmanState_pb2.PacmanState.WALL:
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

def main():
    # The client definition now resides in another file
    # This is a pretty accurate demonstration of normal usage
    s = EngineClient(addr=ADDRESS, port=PORT)
    # "with" uses the context managers to automatically handle connecting
    # and disconnecting the socket cleanly
    with s:
        while True:
            # this will wait until a message has been read
            msg = s.read_msg()
            # but it can return none if there is an error, so check here
            if msg:
                display_game(msg)

if __name__ == "__main__":
    main()
