#!/usr/bin/env python3

import os
import sys
from vision import MovementProcessor

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11297)

def main():
    
    top = ('-t' in sys.argv or os.environ.get("TOP",False))
    bottom = ('-b' in sys.argv or os.environ.get("BOTTOM",False))
    windows = ('-s' in sys.argv or os.environ.get("BOTTOM",False))
    if not (top or bottom):
        print('select either -t for top cam of -b for bottom cam')
        sys.exit(1)
    if top:
        processor = MovementProcessor(ADDRESS, PORT, 1, 15, 15, 26, windows)
    elif bottom:
        processor = MovementProcessor(ADDRESS, PORT, 2, 1, 15, 26, windows)
    processor.run()

if __name__ == "__main__":
    main()
