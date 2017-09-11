import sys
from variables import *

class TerminalPrinter:

    def __init__(self):
        return

    def _parse_game_state(self, state):
        if state == frightened:
            return 'frightened'
        elif state == chase:
            return 'chase'
        elif state == scatter:
            return 'scatter'
        else:
            return 'undefined'

    def _clear_rows(self, rows_count):
        for row in range(rows_count+40):
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K")

    def display_game(self, game_state):
        self._clear_rows(len(game_state.grid[0]))
        state = self._parse_game_state(game_state.state)
        print("Pacman  Score: " + str(game_state.score) + "  State: " + str(state) + "  Lives: " + str(game_state.lives))
        displayBuf = []
        for row_index, row in enumerate(game_state.grid):
            curRow = []
            for col in range(len(row)):
                if (row_index,col) == game_state.pacbot.pos:
                    curRow.append('P')
                elif (row_index,col) == game_state.red.pos["current"] or (row_index,col) == game_state.pink.pos["current"] or (row_index,col) == game_state.orange.pos["current"] or (row_index,col) == game_state.blue.pos["current"]:
                    curRow.append('G')
                elif game_state.grid[row_index][col] == o:
                    curRow.append('.')
                elif game_state.grid[row_index][col] == O:
                    curRow.append('o')
                elif game_state.grid[row_index][col] == e or game_state.grid[row_index][col] == n:
                    curRow.append(' ')
                elif game_state.grid[row_index][col] == I:
                    curRow.append('0')
            displayBuf.append(curRow)
        inverted = zip(*displayBuf)
        for row in reversed(list(inverted)):
            for el in row:
                print(el, end='')
            print()
