#!/usr/bin/env python3

import os, sys
from graphics import Visualizer
from graphics.variables import Split

ADDRESS = os.environ.get("ADDRESS","localhost")
PORT = os.environ.get("SERVER_PORT", 11297)

def main():
    walls = ('-w' in sys.argv or os.environ.get("WALLS",False))
    pacman = ('-p' in sys.argv or os.environ.get("PACMAN",False))
    top = ('-t' in sys.argv or os.environ.get("TOP",False))
    bottom = ('-b' in sys.argv or os.environ.get("BOTTOM",False))
    split = Split.FULL
    if top:
        split = Split.TOP
    elif bottom:
        split = Split.BOTTOM
    visualizer = Visualizer(ADDRESS, PORT, walls, pacman, split)
    visualizer.run()

if __name__ == "__main__":
    main()
