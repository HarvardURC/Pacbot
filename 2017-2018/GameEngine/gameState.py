from variables import *
from solver import *
from ghostpaths import *
from ghostAgent import *
from pacbot import *
from grid import grid
import copy

class GameState:
    def __init__(self):
        self.pacbot = PacBot()
        self.red = ghostAgent(red_init_pos[0], red_init_pos[1], red_init_npos[0], red_init_npos[1], red, red_init_dir, self, [], red_scatter_pos)
        self.pink = ghostAgent(pink_init_pos[0], pink_init_pos[1], pink_init_npos[0], pink_init_npos[1], pink, pink_init_dir, self, pink_start_path. pink_scatter_pos)
        self.orange = ghostAgent(orange_init_pos[0], orange_init_pos[1], orange_init_npos[0], orange_init_npos[1], orange, red_init_dir, self, orange_start_path, orange_scatter_pos)
        self.blue = ghostAgent(blue_init_pos[0], blue_init_pos[1], blue_init_npos[0], blue_init_npos[1], blue, blue_init_dir, self, blue_start_path, blue_scatter_pos)
        self.restart()

    def __become_frightened__(self):
        if state == frightened:
            self.old_state = self.state
            self.frightened_counter = frightened_length
            self.red.become_frightened()
            self.pink.become_frightened()
            self.orange.become_frightened()
            self.blue.become_frightened()

    def __end_frightened__(self):
        self.state = self.old_state
        self.frightened_multiplier = 1

    def __update_ghosts__(self):
        self.red.update()
        self.orange.update()
        self.pink.update()
        self.blue.update()

    def __is_eating_pellet__():
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == o

    def __is_eating_power_pellet__():
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == O

    def __eat_pellet__():
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += pellet_score

    def __eat_power_pellet():
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += power_pellet_score
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
            self.state_counter =
            self.lives -= 1
            self.old_state = chase
            self.state = scatter
            self.frightened_counter = 0
            self.frightened_multiplier = 1
            self.play = False
            self.__update_score__()
        else:
            self.play = False
            print("Success: " + str(self.score))

    def __should_die__(self):
        return (self.red.pos["current"] == self.pacbot.pos and self.red.frightened_counter == 0) or
        (self.pink.pos["current"] == self.pacbot.pos and self.pink.frightened_counter == 0) or
        (self.orange.pos["current"] == self.pacbot.pos and self.orange.frightened_counter == 0) or
        (self.blue.pos["current"] == self.pacbot.pos and self.blue.frightened_counter == 0)

    def __check_if_ghosts_eaten__(self):
        self.__check_if_ghost_eaten__(self.red)
        self.__check_if_ghost_eaten__(self.pink)
        self.__check_if_ghost_eaten__(self.orange)
        self.__check_if_ghost_eaten__(self.blue)

    def __check_if_ghost_eaten__(self, ghost):
        if ghost.pos["current"] == self.pacbot.pos and ghost.frightened_counter > 0:
            ghost.send_home()
            self.score += ghost_score * self.frightened_multiplier
            self.frightened_multiplier += 1

    def __swap_state_if_necessary__(self):
        if self.state_counter in state_swap_times:
            if self.state == chase:
                self.state = scatter
            else:
                self.state = chase

    def next_step(self):
        self.__update_ghosts__()

        if self.__should_die__():
            self.__die__()
        else:
            self.__check_if_ghosts_eaten__()
            if self.state == frightened:
                if self.frightened_counter == 1:
                    self.__end_frightened__()
                self.frightened_counter -= 1
            else:
                self.state_counter += 1

            self.__swap_state_if_necessary__()

            self.__update_score__()
            self.start_counter += 1

    def restart(self):
        self.grid = copy.deepcopy(grid)
        self.old_state = chase
        self.state = scatter
        self.frightened_counter = 0
        self.frightened_multiplier = 1
        self.__respawn_agents__()
        self.score = 0
        self.play = False
        self.start_counter = 0
        self.state_counter = 0
        self.lives = starting_lives
        self.__update_score__():
