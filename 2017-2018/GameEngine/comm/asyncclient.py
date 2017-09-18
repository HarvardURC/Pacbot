
from .pacmanState_pb2 import PacmanState
import struct, asyncio

MAGIC_HEADER = 11297
SIZE_HEADER = struct.Struct("!HH")

class AsyncClient(asyncio.Protocol):
    def __init__(self, addr, port, cb, loop=None):
        """
        cb must be a function that takes a single argument and processes it
        
        Do not do long-running operations in the update function without
        using asynchronous methods. It will be called once for each received
        message, possibly multiple times a tick.
        """
        super().__init__()
        self.loop = loop or asyncio.get_event_loop()
        self.addr = addr
        self.port = port
        self.update = cb
        
    def connect(self):
        coro = asyncio.create_connection(lambda: self, self.addr, self.port)
        self.loop.run_until_complete(coro)

    def connection_made(self, transport):
        self.__length = 0
        self.__buffer = b""
        self.transport = transport

    def connection_lost(self, exception):
        if exception:
            print(repr(exception))
        self.loop.call_soon(self.connect)

    def data_received(self, data):
        self.__buffer += data

        while self.__buffer:
            if not self.__length and len(self.__buffer) > SIZE_HEADER.size:
                magic, length = SIZE_HEADER.unpack(
                    self.__buffer[:SIZE_HEADER.size])
                self.__buffer = self.__buffer[SIZE_HEADER:]
                if magic != MAGIC_NUMBER:
                    self.transport.close()
                    return
            elif self.__length and len(self.__buffer) >= self.__length:
                msg = PacmanState()
                msg.ParseFromString(self.__buffer[:self.__length])
                self.__buffer = self.__buffer[self.__length:]
                self.__length = 0
                self.update(msg)
            else:
                # Not enough data has been buffered and read to form a complete
                # header or message
                return

    # Yay also a context manager
    __enter__ = connect
    def __exit__(self, *args):
        self.transport.close()
