from variables import *
from solver import *
from ghostpaths import *
from agentState import *
from grid import grid
import copy

scared_clicks = 8

class GameState:
    def __init__(self, pacbot):
        self.pacbot = pacbot
        self.red = AgentState(11,13,11,12, 'red',left, -1)
        self.pink = AgentState(15,14,14,14, 'pink',up, 3)
        self.orange = AgentState(15,15,14,15,'orange',up, 40)
        self.blue = AgentState(15,12,14,12,'blue',up, 24)
        self.restart(self)

    def __change_state__(self,state):
        if state == frightened:
            self.frightened_counter = 13
        self.state = state

    def __update_ghost__(self, ghost, start_path = None):
        if self.start_counter < ghost.start_delay:
            ghost.update(start_path[self.start_counter])
        elif ghost.scared_counter < scared_clicks:
            ghost.update(scared_path[ghost.scared_counter])
            ghost.scared_counter += 1
        else:
            ghost.update(next_move(self.pacbot, ghost, self.grid, self.state, scattered = (self.state == scattered)))

    def __update_ghosts__(self):
        self.__update_ghost__(self.red)
        self.__update_ghost__(self.orange, orange_path)
        self.__update_ghost__(self.blue, blue_path)
        self.__update_ghost__(self.pink, pink_path)

    def __is_eating_pellet__():
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == o

    def __is_eating_power_pellet__():
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == O

    def __eat_pellet__():
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += 10

    def __eat_power_pellet():
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += 50
        self.__change_state__(frightened)

    def __update_score__(self):
        if self.__is_eating_pellet__():
            self.__eat_pellet__()

        if self.__is_eating_power_pellet__():
            self.__eat_power_pellet__()

    def __respawn_agents__(self):
        self.pacbot.respawn()
        self.red.respawn()
        self.pink.respawn()
        self.orange.respawn()
        self.blue.respawn()

    def __die__(self):
        if self.lives > 1:
            self.__respawn_agents__()
            self.start_counter = 0
            self.lives -= 1
            self.__update_score__()
            self.play = False
        else:
            self.play = False
            print("Success: " + str(self.score))

    def __should_die__(self):
        return self.red.pos["current"] == self.pacbot.pos or
        self.pink.pos["current"] == self.pacbot.pos or
        self.orange.pos["current"] == self.pacbot.pos or
        self.blue.pos["current"] == self.pacbot.pos

    def __check_if_ghosts_eaten__(self):
        self.__check_if_ghost_eaten__(self.red)
        self.__check_if_ghost_eaten__(self.pink)
        self.__check_if_ghost_eaten__(self.orange)
        self.__check_if_ghost_eaten__(self.blue)

    def __check_if_ghost_eaten__(self, ghost):
        if ghost.pos["current"] == self.pacbot.pos:
            ghost.send_home()
            self.score += 200 * self.frightened_multiplier
            self.frightened_multiplier += 1

    def next_step(self):
        self.__update_ghosts__()

        if self.state == frightened:
            self.__check_if_ghosts_eaten__()

            if self.frightened_counter == 1:
                self.__change_state__(chase)
                self.frightened_multiplier = 1
            self.frightened_counter -= 1

        self.__update_score__()
        self.start_counter += 1

    def restart(self):
        self.grid = copy.deepcopy(grid)
        self.__respawn_agents__()
        self.score = 0
        self.play = False
        self.counter = 0
        self.start_counter = 0
        self.frightened_counter = 0
        self.frightened_multiplier = 1
        self.lives = 3
        self.__change_state__(scatter)
        self.__update_score__():
