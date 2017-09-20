
from .pacmanState_pb2 import PacmanState
import struct, asyncio

from .asyncproto import AsyncProto

class AsyncClient(AsyncProto):
    def __init__(self, addr, port, cb, loop=None):
        """
        cb must be a function that takes a single argument and processes it
        
        Do not do long-running operations in the update function without
        using asynchronous methods. It will be called once for each received
        message, possibly multiple times a "tick".
        """
        super().__init__()
        self.loop = loop or asyncio.get_event_loop()
        self.addr = addr
        self.port = port
        self.update = cb
        
    def connect(self):
        coro = self.loop.create_connection(lambda: self, self.addr, self.port)

        # this part is a little messy I'm not sure what's up with it
        # I can't promise it works if the loop is already running, which would
        # be the case if the connection dropped and tried to reconnect
        # the client can always be manually restarted though, of course.
        if not self.loop.is_running():
            self.loop.run_until_complete(coro)

    def msg_received(self, data):
        msg = PacmanState()
        msg.ParseFromString(data)
        self.update(msg)
            
    # Yay also a context manager
    __enter__ = connect
    def __exit__(self, *args):
        self.transport.close()
