from pacbot.variables import *
from . import pacmanState_pb2

class StateConverter:
    @classmethod
    def _parse_game_mode(cls, mode):
        if mode == scatter:
            return  pacmanState_pb2.PacmanState.SCATTER
        elif mode == chase:
            return  pacmanState_pb2.PacmanState.CHASE
        else:
            return  pacmanState_pb2.PacmanState.FRIGHTENED

    @classmethod
    def _parse_grid_element(cls, el):
        if el == I:
            return pacmanState_pb2.PacmanState.WALL
        elif el == o:
            return pacmanState_pb2.PacmanState.PELLET
        elif el == O:
            return pacmanState_pb2.PacmanState.POWER_PELLET
        else:
            return pacmanState_pb2.PacmanState.EMPTY

    @classmethod
    def _parse_direction(cls, direction):
        if direction == right:
            return pacmanState_pb2.PacmanState.RIGHT
        elif direction == left:
            return pacmanState_pb2.PacmanState.LEFT
        elif direction == up:
            return pacmanState_pb2.PacmanState.UP
        else:
            return pacmanState_pb2.PacmanState.DOWN





    @classmethod
    def convert_game_state_to_proto(cls, game_state):
        proto = pacmanState_pb2.PacmanState()
        proto.mode = StateConverter._parse_game_mode(game_state.state)
        proto.frightened_timer = game_state.frightened_counter
        proto.score = game_state.score
        proto.grid_columns = len(game_state.grid[0])
        proto.lives = game_state.lives

        proto.red_ghost.x = game_state.red.pos['current'][0]
        proto.red_ghost.y = game_state.red.pos['current'][1]
        proto.red_ghost.direction = StateConverter._parse_direction(game_state.red.direction)

        proto.pink_ghost.x = game_state.pink.pos['current'][0]
        proto.pink_ghost.y = game_state.pink.pos['current'][1]
        proto.pink_ghost.direction = StateConverter._parse_direction(game_state.pink.direction)

        proto.orange_ghost.x = game_state.orange.pos['current'][0]
        proto.orange_ghost.y = game_state.orange.pos['current'][1]
        proto.orange_ghost.direction = StateConverter._parse_direction(game_state.orange.direction)

        proto.blue_ghost.x = game_state.blue.pos['current'][0]
        proto.blue_ghost.y = game_state.blue.pos['current'][1]
        proto.blue_ghost.direction = StateConverter._parse_direction(game_state.blue.direction)

        proto.pacman.x = game_state.pacbot.pos[0]
        proto.pacman.y = game_state.pacbot.pos[1]
        proto.pacman.direction = StateConverter._parse_direction(game_state.pacbot.direction)

        for col in game_state.grid:
            for el in col:
                proto.grid.append(StateConverter._parse_grid_element(el))

        return proto
