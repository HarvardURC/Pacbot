import asyncio
from robomodules.comm.asyncClient import AsyncClient
from robomodules.comm.subscribe_pb2 import Subscribe

class ProtoModule:
    def __init__(self, addr, port, message_buffers, MsgType, subscriptions):
        self.loop = asyncio.get_event_loop()
        self.client = AsyncClient(addr, port, self.msg_received, message_buffers, MsgType, subscriptions, self.loop)
        self.loop.call_soon(self.tick)

    def tick(self):
        raise NotImplementedError()

    def msg_received(self, msg, msg_type):
        raise NotImplementedError()

    def subscribe(self, msg_types):
        self.client.subscribe(msg_types, Subscribe.SUBSCRIBE)

    def unsubscribe(self, msg_types):
        self.client.subscribe(msg_types, Subscribe.UNSUBSCRIBE)

    def write(self, msg, msg_type):
        self.client.write(msg, msg_type)
    
    def run(self):
        try:
            with self.client:
                self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        self.loop.stop()
