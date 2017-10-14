from enum import Enum
from .lightState_pb2 import LightState

class MsgType(Enum):
    LIGHT_STATE = 0

message_buffers = {
    MsgType.LIGHT_STATE: LightState
}


__all__ = ['MsgType', 'message_buffers', 'LightState']
