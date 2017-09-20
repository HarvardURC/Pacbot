#!/usr/bin/env python3

import asyncio, os

from comm import pack_msg
from vision import MovementProcessor

ADDRESS = os.environ.get("SERVER_ADDRESS","127.0.0.1")
PORT = os.environ.get("SERVER_PORT", 11295)

class InputClient:
    def __init__(self, loop):
        self.loop = loop
        coro = asyncio.open_connection(ADDRESS, PORT, loop=loop)
        _, self.writer = loop.run_until_complete(coro)

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
        
def main():
    loop = asyncio.get_event_loop()
    client = InputClient(loop)
    processor = MovementProcessor(client, loop)
    client.run()

if __name__ == "__main__":
    main()
