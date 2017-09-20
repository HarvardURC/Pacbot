
# the opencv import prevents this module from being loaded and used for me
import asyncio, opencv

class MovementProcessor:
    def __init__(self, client, loop=None):
        self.client = client
        self.loop = loop or asyncio.get_event_loop()
        self.loop.call_soon(self.tick)

    def tick(self):
        msg = None
        self.client.write(msg)
        self.call_later(1/60, self.tick)
