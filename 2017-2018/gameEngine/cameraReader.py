#!/usr/bin/env python3

import os
from vision import MovementProcessor

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11297)

def main():
    processor = MovementProcessor(ADDRESS, PORT, 0)
    processor.run()

if __name__ == "__main__":
    main()
