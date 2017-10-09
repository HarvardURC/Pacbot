#!/usr/bin/env python3

import os, sys
from graphics import Visualizer

ADDRESS = os.environ.get("SERVER_ADDRESS","localhost")
PORT = os.environ.get("SERVER_PORT", 11297)

def main():
    walls = ('-w' in sys.argv or os.environ.get("WALLS",False))
    pacman = ('-p' in sys.argv or os.environ.get("PACMAN",False))
    visualizer = Visualizer(ADDRESS, PORT, walls, pacman)
    visualizer.run()

if __name__ == "__main__":
    main()
