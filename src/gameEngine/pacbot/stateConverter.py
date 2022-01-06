from .variables import *
from messages.pacmanState_pb2 import PacmanState
from messages.lightState_pb2 import LightState
import time

class StateConverter:

    _directions = {}
    _directions[right] = PacmanState.RIGHT
    _directions[left] = PacmanState.LEFT
    _directions[up] = PacmanState.UP
    _directions[down] = PacmanState.DOWN

    @classmethod
    def _parse_game_mode(cls, mode, play):
        if not play:
            return PacmanState.PAUSED
        elif mode == scatter:
            return  PacmanState.SCATTER
        elif mode == chase:
            return  PacmanState.CHASE
        else:
            return  PacmanState.FRIGHTENED

    @classmethod
    def _parse_grid_element(cls, el):
        if el == I:
            return PacmanState.WALL
        elif el == o:
            return PacmanState.PELLET
        elif el == O:
            return PacmanState.POWER_PELLET
        elif el == c:
            return PacmanState.CHERRY
        else:
            return PacmanState.EMPTY

    @classmethod
    def convert_game_state_to_full(cls, game_state):
        proto = PacmanState()
        proto.mode = StateConverter._parse_game_mode(game_state.state, game_state.play)
        proto.frightened_timer = game_state.frightened_counter
        proto.score = game_state.score
        proto.grid_columns = len(game_state.grid[0])
        proto.lives = game_state.lives
        proto.update_ticks = (game_state.update_ticks - 1) % ticks_per_update
        proto.ticks_per_update = ticks_per_update
        proto.elapsed_time = game_state.elapsed_time

        if game_state.play:
            proto.elapsed_time += time.time() - game_state.previous_start

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

        for col in game_state.grid:
            for el in col:
                proto.grid.append(StateConverter._parse_grid_element(el))

        return proto

    @classmethod
    def convert_game_state_to_light(cls, game_state):
        proto = LightState()
        proto.mode = LightState.RUNNING if game_state.play else LightState.PAUSED
        proto.score = game_state.score
        proto.lives = game_state.lives

        proto.red_ghost.x = game_state.red.pos['current'][0]
        proto.red_ghost.y = game_state.red.pos['current'][1]
        proto.red_ghost.state = LightState.FRIGHTENED if game_state.red.frightened_counter > 0 else LightState.NORMAL

        proto.pink_ghost.x = game_state.pink.pos['current'][0]
        proto.pink_ghost.y = game_state.pink.pos['current'][1]
        proto.pink_ghost.state = LightState.FRIGHTENED if game_state.pink.frightened_counter > 0 else LightState.NORMAL

        proto.orange_ghost.x = game_state.orange.pos['current'][0]
        proto.orange_ghost.y = game_state.orange.pos['current'][1]
        proto.orange_ghost.state = LightState.FRIGHTENED if game_state.orange.frightened_counter > 0 else LightState.NORMAL

        proto.blue_ghost.x = game_state.blue.pos['current'][0]
        proto.blue_ghost.y = game_state.blue.pos['current'][1]
        proto.blue_ghost.state = LightState.FRIGHTENED if game_state.blue.frightened_counter > 0 else LightState.NORMAL

        proto.pacman.x = game_state.pacbot.pos[0]
        proto.pacman.y = game_state.pacbot.pos[1]

        proto.cherry = game_state.cherry

        return proto
