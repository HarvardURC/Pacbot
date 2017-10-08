import struct, asyncio
from enum import Enum
from .asyncProto import AsyncProto
from .subscribe_pb2 import Subscribe
from .constants import _SUBSCRIBE

class AsyncClient(AsyncProto):
    def __init__(self, addr, port, cb, message_buffers, MsgType, subscriptions, loop=None):
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
        self.subscriptions = subscriptions
        self.update = cb
        self.MsgType = MsgType
        self.message_buffers = message_buffers

    def connect(self):
        coro = self.loop.create_connection(lambda: self, self.addr, self.port)

        # this part is a little messy I'm not sure what's up with it
        # I can't promise it works if the loop is already running, which would
        # be the case if the connection dropped and tried to reconnect
        # the client can always be manually restarted though, of course.
        if not self.loop.is_running():
            self.loop.run_until_complete(coro)

    def connection_made(self, transport):
        super().connection_made(transport)
        if len(self.subscriptions) > 0:
            self.subscribe(self.subscriptions, Subscribe.SUBSCRIBE)

    def msg_received(self, data, msg_type):
        if msg_type != _SUBSCRIBE:
            msg = self.message_buffers[self.MsgType(msg_type)]()
            msg.ParseFromString(data)
            self.update(msg, self.MsgType(msg_type))

    def write(self, msg, msg_type):
        super().write(msg, msg_type)

    def subscribe(self, msg_types, direction):
        msg = Subscribe()
        for msg_type in msg_types:
            msg.msg_types.append(msg_type.value)
        msg.dir = direction
        self.write(msg.SerializeToString(), _SUBSCRIBE)


    # Yay also a context manager
    __enter__ = connect
    def __exit__(self, *args):
        self.transport.close()
