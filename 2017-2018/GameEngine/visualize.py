#!/usr/bin/env python3

import asyncio, os

from graphics import Visualizer
from comm import AsyncClient

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11297)

def main():
    loop = asyncio.get_event_loop()
    visualizer = Visualizer()
    client = AsyncClient(ADDRESS, PORT, visualizer.update, loop)

    with client:
        loop.run_forever()

if __name__ == "__main__":
    main()
