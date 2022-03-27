import os, copy
import robomodules as rm
from messages import MsgType, message_buffers

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60



class BasicHighLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        