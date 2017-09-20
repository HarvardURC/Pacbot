
import asyncio

from .constants import MAGIC_HEADER, SIZE_HEADER

class AsyncProto(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.__length = 0
        self.__buffer = b""

    def connection_lost(self, exception):
        if exception:
            print(repr(exception))

    def data_received(self, data):
        self.__buffer += data

        while self.__buffer:
            if not self.__length and len(self.__buffer) > SIZE_HEADER.size:
                magic, self.__length = SIZE_HEADER.unpack(
                    self.__buffer[:SIZE_HEADER.size])
                self.__buffer = self.__buffer[SIZE_HEADER.size:]
                if magic != MAGIC_HEADER:
                    self.transport.close()
                    self.loop.call_soon(self.connect)
                    return
            elif self.__length and len(self.__buffer) >= self.__length:
                self.msg_received(self.__buffer[:self.__length])
                self.__buffer = self.__buffer[self.__length:]
                self.__length = 0
            else:
                # Not enough data has been buffered and read to form a complete
                # header or message
                return

    def msg_received(self, data):
        raise NotImplementedError()
