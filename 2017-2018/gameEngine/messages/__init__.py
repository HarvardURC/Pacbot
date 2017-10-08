from enum import Enum
from .mockMsg_pb2 import MockMsg
from .pacmanState_pb2 import PacmanState

class MsgType(Enum):
    MOCK_MSG = 0
    FULL_STATE = 1
    PACMAN_LOCATION = 2 

message_buffers = {
    MsgType.MOCK_MSG: MockMsg,
    MsgType.FULL_STATE: PacmanState,
    MsgType.PACMAN_LOCATION: PacmanState.AgentState
}


__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'PacmanState']
