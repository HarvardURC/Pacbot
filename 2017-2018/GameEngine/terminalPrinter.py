import sys
from variables import *
import pacmanState_pb2
import time

def get_game_state():
    # TODO: Get game state through a socket
    return pacmanState_pb2.PacmanState()

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
        if (row_index,col_index) == (state.pacman.x, state.pacman.y)
            cur_row.append('P')
        elif (row_index,col_index) == (state.red_ghost.x, state.red_ghost.y) or (row_index,col_index) == (state.orange_ghost.x, state.orange_ghost.y) or (row_index,col_index) == (state.pink_ghost.x, state.pink_ghost.y) or (row_index,col_index) == (state.blue_ghost.x, state.blue_ghost.y):
            cur_row.append('G')
        elif el == pacmanState_pb2.PacmanState.PELLET
            cur_row.append('.')
        elif el == pacmanState_pb2.PacmanState.POWER_PELLET
            cur_row.append('o')
        elif el == pacmanState_pb2.PacmanState.EMPTY
            cur_row.append(' ')
        elif el == pacmanState_pb2.PacmanState.WALL
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

def main():
    while True:
        state = get_game_state()
        display_game(state)
        time.sleep(1.0/10)

if __name__ == "__main__":
    main()
