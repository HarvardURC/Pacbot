
import asyncio, sys

class MovementProcessor:
    def __init__(self, client, loop=None):
        self.client = client
        self.loop = loop or asyncio.get_event_loop()
        self.loop.add_reader(sys.stdin, self.keypress)

    def keypress(self):
        char = sys.stdin.read(1)
        if char == "a":
            self.client.write(b"left") # except write a proper binary message
        elif char == "d":
            self.client.write(b"right") # except write a proper binary message
        elif char == "q":
            self.client.quit()
