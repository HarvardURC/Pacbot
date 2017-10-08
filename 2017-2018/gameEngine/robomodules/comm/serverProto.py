from enum import Enum
import struct, asyncio
from .asyncProto import AsyncProto

class ServerProto(AsyncProto):
    def __init__(self, parent, loop=None):
        super().__init__()
        self.loop = loop or asyncio.get_event_loop()
        self.parent = parent

    def connection_made(self, transport):
        super().connection_made(transport)
        self.parent.clients.append(self)

    def connection_lost(self, exc):
        self.parent.remove_client(self)

    def msg_received(self, data, msg_type):
        self.parent.msg_received(self, data, msg_type)
