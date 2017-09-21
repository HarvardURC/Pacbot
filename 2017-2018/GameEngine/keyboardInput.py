#!/usr/bin/env python3

import asyncio, sys, os, curses

from comm import pack_msg

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11295)

class InputClient:
    def __init__(self, loop):
        self.loop = loop
        coro = asyncio.open_connection(ADDRESS, PORT, loop=loop)
        _, self.writer = loop.run_until_complete(coro)
        self.loop.add_reader(sys.stdin, self.keypress)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        self.writer.close()
        self.loop.stop()

    def write(self, msg):
        self.writer.write(pack_msg(msg))

    def keypress(self):
        char = sys.stdin.read(1)
        if char == "a":
            self.write(b"left") # except write a proper binary message
        elif char == "d":
            self.write(b"right") # except write a proper binary message
        elif char == "q":
            self.quit()
        
def main():
    loop = asyncio.get_event_loop()
    client = InputClient(loop)
    curses.wrapper(lambda scr: client.run())

if __name__ == "__main__":
    main()
