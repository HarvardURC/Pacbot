from enum import Enum
from .pacmanState_pb2 import PacmanState

class MsgType(Enum):
    FULL_STATE = 0
    PACMAN_LOCATION = 1

message_buffers = {
    MsgType.FULL_STATE: PacmanState,
    MsgType.PACMAN_LOCATION: PacmanState.AgentState
}


__all__ = ['MsgType', 'message_buffers', 'PacmanState']
