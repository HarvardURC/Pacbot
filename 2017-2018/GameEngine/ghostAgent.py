from ghostpaths import *
import math
from variables import *

class GhostAgent:

    def __init__(self, x1, y1, x2, y2, color, direction, game_state, start_path, scatter_pos):
        self.color = color
        self.init_direction = direction
        self.init_moves = [x1, y1, x2, y2]
        self.respawn_counter = len(respawn_path)
        self.game_state = game_state
        self.start_path = start_path
        self.scatter_pos = scatter_pos
        self.frightened_counter = 0

    def __is_move_legal__(self, move):
        return move != self.pos["current"] and
            self.game_state.grid[move[0]][move[1]] != I and
            self.game_state.grid[move[0]][move[1]] != n:

    def __find_possible_moves__(self):
        (x,y) = self.pos['next']
        possible=[]
        if self.__is_move_legal__((x+1, y)):
            possible.append((x+1,y))
        if self.__is_move_legal__((x, y+1)) and (x,y) not in ghost_no_up_tiles:
            possible.append((x,y+1))
        if self.__is_move_legal__((x-1, y)):
            possible.append((x-1,y))
        if self.__is_move_legal__((x, y-1)):
            possible.append((x,y-1))
        if possible == []:
            possible.append(self.pos["current"])
        return possible

    def __get_direction__(pos_prev, pos_new):
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

    def __get_next_blue_chase_move__(self):
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

        return self.__get_move_based_on_target__((x,y))

    def __get_next_pink_chase_move__():
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

        return self.__get_move_based_on_target__((x,y))

    def __get_next_red_chase_move__():
        return self.__get_move_based_on_target__(self.game_state.pacbot.pos)

    def __get_next_orange_chase_move__():
        if self.__get_euclidian_distance__(self.pos["current"], self.game_state.pacbot.pos) > 8:
            return self.__get_next_scatter_move__()
        return self.__get_move_based_on_target__(self.game_state.pacbot.pos)

    def __get_move_based_on_target__(self, target):
        possible = self.__find_possible_moves__()
        for tile in possible:
            distances.append(self.__get_euclidian_distance__(target, tile))
        (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))

        return (possible[index], self.__get_direction__(self.pos["next"], possible[index]))

    def __get_next_chase_move__(self):
        if self.color == blue:
            return self.__get_next_blue_chase_move__()
        elif ghost.color == pink:
            return self.__get_next_pink_chase_move__()
        elif ghost.color == red:
            return self.__get_next_red_chase_move__()
        else:
            return self.__get_next_orange_chase_move__()

    def __get_next_scatter_move__(self):
        return self.__get_move_based_on_target__(self.scatter_pos)

    def __get_next_frightened_move__(self):
        possible = self.__find_possible_moves__()
        move = random.choice(possible)
        return (move, self.__get_direction__(self.pos["next"], move))

    def __get_next_state_move__(self):
        if self.frightened_counter > 0:
            return self.__get_next_frightened_move__()
        elif state == chase:
            return self.__get_next_chase_move__()
        else
            return self.__get_next_scatter_move__()

    def __get_euclidian_distance__(pos_a, pos_b):
        return math.hypot(int(pos_a[0])-int(pos_b[0]), int(pos_a[1])-int(pos_b[1]))

    def __should_follow_starting_path__(self):
        return self.game_state.start_counter < len(self.start_path)

    def __should_follow_respawn_path__(self):
        return self.respawn_counter < len(respawn_path)

    def __follow_respawn_path__(self):
        self.update(respawn_path[self.respawn_counter])
        self.respawn_counter += 1

    def __decide_next_moves__(self):
        if self.__should_follow_starting_path__():
            return self.start_path[self.start_counter]
        elif self.__should_follow_respawn_path__():
            self.respawn_counter += 1
            return respawn_path[self.respawn_counter]
        else:
            return self.__get_next_state_move__()

    def update(self):
        if self.frightened_counter > 0:
            self.frightened_counter -= 1
        next_moves = self.__decide_next_moves__()
        self.pos['current'] = self.pos['next']
        self.pos['next'] = next_moves[0]
        self.direction = next_moves[1]

    def send_home(self):
        self.pos['current'] = ghost_home_pos
        self.pos['next'] = (ghost_home_pos[0], ghost_home_pos[1]+1)
        self.direction = up
        self.respawn_path = 0
        self.frightened_counter = 0

    def become_frightened(self):
        self.frightened_counter = frightened_length

    def respawn(self):
        self.pos = {
            'current' : (self.init_moves[0], self.init_moves[1]),
            'next' : (self.init_moves[2],self.init_moves[3])
        }
        self.direction = self.init_direction
        self.scared_counter = 0
        self.respawn_counter = len(respawn_path)
