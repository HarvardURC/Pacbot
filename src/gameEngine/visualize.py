#!/usr/bin/env python3

import os, sys
from graphics import Visualizer
from graphics.variables import Split
from graphics.variables import TOP_SQUARE_SIZE, BOTTOM_SQUARE_SIZE, SQUARE_SIZE

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

def main():
    square_size = SQUARE_SIZE

    walls = ('-w' in sys.argv or os.environ.get("WALLS",False))
    pacman = ('-p' in sys.argv or os.environ.get("PACMAN",False))
    top = ('-t' in sys.argv or os.environ.get("TOP",False))
    bottom = ('-b' in sys.argv or os.environ.get("BOTTOM",False))
    split = Split.FULL
    if top:
        split = Split.TOP
        square_size = TOP_SQUARE_SIZE
    elif bottom:
        split = Split.BOTTOM
        square_size = BOTTOM_SQUARE_SIZE


    # If the command was run with the argument "-s=x" then set the square size to x
    # If the command was run with the argument "-s" then make the square size 25
    # This allows the game to be rendered correctly on most normal computer screens
    for arg in sys.argv:
        if arg[0:3] == '-s=' and arg[3:].isnumeric():
            square_size = int(arg[3:])
            break
        elif arg[0:2] == '-s' and square_size == SQUARE_SIZE:
            square_size = 25

    visualizer = Visualizer(ADDRESS, PORT, walls, pacman, split, square_size)
    visualizer.run()

if __name__ == "__main__":
    main()
