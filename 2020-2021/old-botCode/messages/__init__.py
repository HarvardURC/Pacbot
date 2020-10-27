from enum import Enum
from .lightState_pb2 import LightState
from .pacmanState_pb2 import PacmanState
from .pacmanCommand_pb2 import PacmanCommand


class MsgType(Enum):
    LIGHT_STATE = 0
    PACMAN_LOCATION = 1
    PACMAN_COMMAND = 2


message_buffers = {
    MsgType.LIGHT_STATE: LightState,
    MsgType.PACMAN_LOCATION: PacmanState.AgentState,
    MsgType.PACMAN_COMMAND: PacmanCommand
}


__all__ = ['MsgType', 'message_buffers', 'LightState', 'PacmanState',
           'PacmanCommand']
