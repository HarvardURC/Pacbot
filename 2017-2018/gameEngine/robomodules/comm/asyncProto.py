import asyncio
from .constants import *
from robomodules.comm import pack_msg

class AsyncProto(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.__length = 0
        self.__buffer = b""
        self.__msg_type = -1

    def connection_lost(self, exception):
        if exception:
            print(repr(exception))

    def data_received(self, data):
        self.__buffer += data

        while self.__buffer:
            if not self.__length and len(self.__buffer) > SIZE_HEADER.size:
                magic, msg_type, self.__length = SIZE_HEADER.unpack(
                    self.__buffer[:SIZE_HEADER.size])
                self.__buffer = self.__buffer[SIZE_HEADER.size:]
                self.__msg_type = msg_type
                if magic != MAGIC_HEADER:
                    self.transport.close()
                    if hasattr(self, "connect"):
                        self.loop.call_soon(self.connect)
                    return
            elif self.__length and len(self.__buffer) >= self.__length:
                self.msg_received(self.__buffer[:self.__length], self.__msg_type)
                self.__buffer = self.__buffer[self.__length:]
                self.__length = 0
                self.__msg_type = -1
            else:
                # Not enough data has been buffered and read to form a complete
                # header or message
                return

    def write(self, msg, msg_type):
        if self.transport:
            self.transport.write(pack_msg(msg, msg_type))

    def msg_received(self, data):
        raise NotImplementedError()
