from enum import Enum
from .lightState_pb2 import LightState
from .pacmanState.proto import PacmanState

class MsgType(Enum):
    LIGHT_STATE = 0
    PACMAN_LOCATION = 1


message_buffers = {
    MsgType.LIGHT_STATE: LightState,
    MsgType.PACMAN_LOCATION: PacmanState.AgentState
}


__all__ = ['MsgType', 'message_buffers', 'LightState', 'PacmanState']
