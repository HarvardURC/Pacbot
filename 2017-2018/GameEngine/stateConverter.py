from variables import *
import pacmanState_pb2

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
    def convert_game_state_to_proto(cls, game_state):
        proto = pacmanState_pb2.PacmanState()
        proto.mode = StateConverter._parse_game_mode(game_state.state)
        proto.frightened_timer = game_state.frightened_counter
        proto.score = game_state.score
        proto.grid_columns = len(game_state.grid)
        proto.lives = game_state.lives

        #proto.red_ghost = pacmanState_pb2.Position()
        proto.red_ghost.x = game_state.red.pos['current'][0]
        proto.red_ghost.y = game_state.red.pos['current'][1]

        #proto.pink_ghost = pacmanState_pb2.Position()
        proto.pink_ghost.x = game_state.pink.pos['current'][0]
        proto.pink_ghost.y = game_state.pink.pos['current'][1]

        #proto.orange_ghost = pacmanState_pb2.Position()
        proto.orange_ghost.x = game_state.orange.pos['current'][0]
        proto.orange_ghost.y = game_state.orange.pos['current'][1]

        #proto.blue_ghost = pacmanState_pb2.Position()
        proto.blue_ghost.x = game_state.blue.pos['current'][0]
        proto.blue_ghost.y = game_state.blue.pos['current'][1]

        #proto.pacman = pacmanState_pb2.Position()
        proto.pacman.x = game_state.pacbot.pos[0]
        proto.pacman.y = game_state.pacbot.pos[1]

        for col in game_state.grid:
            for el in col:
                proto.grid.append(StateConverter._parse_grid_element(el))

        return proto
