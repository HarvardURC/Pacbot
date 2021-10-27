from .ghostpaths import *
from .variables import *
import random
import math

class GhostAgent:

    def __init__(self, x1, y1, x2, y2, color, direction, game_state, start_path, scatter_pos):
        self.color = color
        self.init_direction = direction
        self.init_moves = [x1, y1, x2, y2]
        self.respawn_counter = 0 
        self.game_state = game_state
        self.start_path = start_path
        self.scatter_pos = scatter_pos
        self.frightened_counter = 0

    def _is_move_legal(self, move):
        return (move != self.pos["current"] and
            self.game_state.grid[move[0]][move[1]] != I and
            self.game_state.grid[move[0]][move[1]] != n)

    def _find_possible_moves(self):
        (x,y) = self.pos['next']
        possible=[]
        if self._is_move_legal((x+1, y)):
            possible.append((x+1,y))
        if self._is_move_legal((x, y+1)) and (x,y) not in ghost_no_up_tiles:
            possible.append((x,y+1))
        if self._is_move_legal((x-1, y)):
            possible.append((x-1,y))
        if self._is_move_legal((x, y-1)):
            possible.append((x,y-1))
        if possible == []:
            possible.append(self.pos["current"])
        return possible

    def _get_direction(self, pos_prev, pos_new):
        if pos_new[0] > pos_prev[0]:
            return right
        elif pos_new[0] < pos_prev[0]:
            return left
        elif pos_new[1] > pos_prev[1]:
            return up
        elif pos_new[1] < pos_prev[1]:
            return down
        else:
            return self.direction

    def _get_next_blue_chase_move(self):
        pacbot_target = (0,0)
        if self.game_state.pacbot.direction == up:
            pacbot_target = (self.game_state.pacbot.pos[0], self.game_state.pacbot.pos[1] + 2)
        elif self.game_state.pacbot.direction == down:
            pacbot_target = (self.game_state.pacbot.pos[0], self.game_state.pacbot.pos[1] - 2)
        elif self.game_state.pacbot.direction == left:
            pacbot_target = (self.game_state.pacbot.pos[0] - 2, self.game_state.pacbot.pos[1])
        elif self.game_state.pacbot.direction == right:
            pacbot_target = (self.game_state.pacbot.pos[0] + 2, self.game_state.pacbot.pos[1])
        x = pacbot_target[0] + (pacbot_target[0] - self.game_state.red.pos["current"][0])
        y = pacbot_target[1] + (pacbot_target[1] - self.game_state.red.pos["current"][1])

        return self._get_move_based_on_target((x,y))

    def _get_next_pink_chase_move(self):
        (x,y) = (0,0)

        if self.game_state.pacbot.direction == up:
            x = self.game_state.pacbot.pos[0] - 4
            y = self.game_state.pacbot.pos[1] + 4
        elif self.game_state.pacbot.direction == down:
            x = self.game_state.pacbot.pos[0]
            y = self.game_state.pacbot.pos[1] - 4
        elif self.game_state.pacbot.direction == left:
            x = self.game_state.pacbot.pos[0] - 4
            y = self.game_state.pacbot.pos[1]
        elif self.game_state.pacbot.direction == right:
            x = self.game_state.pacbot.pos[0] + 4
            y = self.game_state.pacbot.pos[1]

        return self._get_move_based_on_target((x,y))

    def _get_next_red_chase_move(self):
        return self._get_move_based_on_target(self.game_state.pacbot.pos)

    def _get_next_orange_chase_move(self):
        if self._get_euclidian_distance(self.pos["current"], self.game_state.pacbot.pos) > 8:
            return self._get_next_scatter_move()
        return self._get_move_based_on_target(self.game_state.pacbot.pos)

    def _get_move_based_on_target(self, target):
        possible = self._find_possible_moves()
        distances = []
        for tile in possible:
            distances.append(self._get_euclidian_distance(target, tile))
        (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))

        return (possible[index], self._get_direction(self.pos["next"], possible[index]))

    def _get_next_chase_move(self):
        if self.color == blue:
            return self._get_next_blue_chase_move()
        elif self.color == pink:
            return self._get_next_pink_chase_move()
        elif self.color == red:
            return self._get_next_red_chase_move()
        else:
            return self._get_next_orange_chase_move()

    def _get_next_scatter_move(self):
        return self._get_move_based_on_target(self.scatter_pos)

    def _get_next_frightened_move(self):
        possible = self._find_possible_moves()
        move = random.choice(possible)
        return (move, self._get_direction(self.pos["next"], move))

    def _get_next_state_move(self):
        if self.frightened_counter > 0:
            return self._get_next_frightened_move()
        elif self.game_state.state == chase:
            return self._get_next_chase_move()
        else:
            return self._get_next_scatter_move()

    def _get_euclidian_distance(self, pos_a, pos_b):
        return math.hypot(int(pos_a[0])-int(pos_b[0]), int(pos_a[1])-int(pos_b[1]))

    def _should_follow_starting_path(self):
        return self.game_state.start_counter < len(self.start_path)

    def _should_follow_respawn_path(self):
        return self.respawn_counter < len(respawn_path)

    def _decide_next_moves(self):
        if self._should_follow_starting_path():
            return self.start_path[self.game_state.start_counter]
        elif self._should_follow_respawn_path():
            self.respawn_counter += 1
            return respawn_path[self.respawn_counter-1]
        else:
            return self._get_next_state_move()

    def update(self):
        if self.frightened_counter > 0:
            self.frightened_counter -= 1
        next_moves = self._decide_next_moves()
        self.pos['current'] = self.pos['next']
        self.pos['next'] = next_moves[0]
        self.direction = next_moves[1]

    def send_home(self):
        self.pos['current'] = ghost_home_pos
        self.pos['next'] = (ghost_home_pos[0], ghost_home_pos[1]+1)
        self.direction = up
        self.respawn_counter = 0
        self.frightened_counter = 0

    def become_frightened(self):
        self.frightened_counter = frightened_length

    def is_frightened(self):
        return self.frightened_counter > 0

    def respawn(self):
        self.pos = {
            'current' : (self.init_moves[0], self.init_moves[1]),
            'next' : (self.init_moves[2],self.init_moves[3])
        }
        self.direction = self.init_direction
        self.scared_counter = 0
        self.respawn_counter = len(respawn_path)
