from pacbot.variables import *
from . import pacmanState_pb2
import time

class StateConverter:

    _directions = {}
    _directions[right] = pacmanState_pb2.PacmanState.RIGHT
    _directions[left] = pacmanState_pb2.PacmanState.LEFT
    _directions[up] = pacmanState_pb2.PacmanState.UP
    _directions[down] = pacmanState_pb2.PacmanState.DOWN

    @classmethod
    def _parse_game_mode(cls, mode, play):
        if not play:
            return pacmanState_pb2.PacmanState.PAUSED
        elif mode == scatter:
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
    def convert_game_state_to_proto(cls, game_state):
        proto = pacmanState_pb2.PacmanState()
        proto.mode = StateConverter._parse_game_mode(game_state.state, game_state.play)
        proto.frightened_timer = game_state.frightened_counter
        proto.score = game_state.score
        proto.grid_columns = len(game_state.grid[0])
        proto.lives = game_state.lives
        proto.update_ticks = (game_state.update_ticks - 1) % ticks_per_update
        proto.ticks_per_update = ticks_per_update 

        proto.red_ghost.x = game_state.red.pos['current'][0]
        proto.red_ghost.y = game_state.red.pos['current'][1]
        proto.red_ghost.direction = StateConverter._directions[game_state.red.direction]
        proto.red_ghost.frightened_counter = game_state.red.frightened_counter

        proto.pink_ghost.x = game_state.pink.pos['current'][0]
        proto.pink_ghost.y = game_state.pink.pos['current'][1]
        proto.pink_ghost.direction = StateConverter._directions[game_state.pink.direction]
        proto.pink_ghost.frightened_counter = game_state.pink.frightened_counter

        proto.orange_ghost.x = game_state.orange.pos['current'][0]
        proto.orange_ghost.y = game_state.orange.pos['current'][1]
        proto.orange_ghost.direction = StateConverter._directions[game_state.orange.direction]
        proto.orange_ghost.frightened_counter = game_state.orange.frightened_counter

        proto.blue_ghost.x = game_state.blue.pos['current'][0]
        proto.blue_ghost.y = game_state.blue.pos['current'][1]
        proto.blue_ghost.direction = StateConverter._directions[game_state.blue.direction]
        proto.blue_ghost.frightened_counter = game_state.blue.frightened_counter

        proto.pacman.x = game_state.pacbot.pos[0]
        proto.pacman.y = game_state.pacbot.pos[1]
        proto.pacman.direction = StateConverter._directions[game_state.pacbot.direction]
        proto.elapsed_time = game_state.elapsed_time 

        if game_state.play:
            proto.elapsed_time += time.time() - game_state.previous_start

        for col in game_state.grid:
            for el in col:
                proto.grid.append(StateConverter._parse_grid_element(el))

        return proto
