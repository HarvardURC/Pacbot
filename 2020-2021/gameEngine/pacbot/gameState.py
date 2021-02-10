from .variables import *
from .ghostpaths import *
from .ghostAgent import *
from .pacbot import *
from .grid import grid
import copy, time

class GameState:
    def __init__(self):
        self.pacbot = PacBot()
        self.red = GhostAgent(red_init_pos[0], red_init_pos[1], red_init_npos[0], red_init_npos[1], red, red_init_dir, self, [], red_scatter_pos)
        self.pink = GhostAgent(pink_init_pos[0], pink_init_pos[1], pink_init_npos[0], pink_init_npos[1], pink, pink_init_dir, self, pink_start_path, pink_scatter_pos)
        self.orange = GhostAgent(orange_init_pos[0], orange_init_pos[1], orange_init_npos[0], orange_init_npos[1], orange, red_init_dir, self, orange_start_path, orange_scatter_pos)
        self.blue = GhostAgent(blue_init_pos[0], blue_init_pos[1], blue_init_npos[0], blue_init_npos[1], blue, blue_init_dir, self, blue_start_path, blue_scatter_pos)
        self.restart()

    def _become_frightened(self):
        if self.state != frightened:
            self.old_state = self.state
        self.state = frightened
        self.frightened_counter = frightened_length
        self.red.become_frightened()
        self.pink.become_frightened()
        self.orange.become_frightened()
        self.blue.become_frightened()

    def _end_frightened(self):
        self.state = self.old_state
        self.frightened_multiplier = 1

    def _update_ghosts(self):
        self.red.update()
        self.orange.update()
        self.pink.update()
        self.blue.update()

    def _is_eating_pellet(self):
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == o

    def _is_eating_power_pellet(self):
        return self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == O

    def _eat_pellet(self):
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += pellet_score
        self.pellets -= 1

    def _eat_power_pellet(self):
        self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
        self.score += power_pellet_score
        self.power_pellets -= 1
        self._become_frightened()

    def _update_score(self):
        if self._is_eating_pellet():
            self._eat_pellet()

        if self._is_eating_power_pellet():
            self._eat_power_pellet()

    def _respawn_agents(self):
        self.pacbot.respawn()
        self.red.respawn()
        self.pink.respawn()
        self.orange.respawn()
        self.blue.respawn()

    def _end_game(self):
        self.play = False
        print("Sore: " + str(self.score))
        print("Time: " + str(self.elapsed_time))

    def _die(self):
        if self.lives > 1:
            self._respawn_agents()
            self.start_counter = 0
            self.state_counter = 0
            self.lives -= 1
            self.old_state = chase
            self.state = scatter
            self.frightened_counter = 0
            self.frightened_multiplier = 1
            self.pause()
            self._update_score()
        else:
            self._end_game() 

    def _should_die(self):
        return ((self.red.pos["current"] == self.pacbot.pos and self.red.frightened_counter == 0) or
        (self.pink.pos["current"] == self.pacbot.pos and self.pink.frightened_counter == 0) or
        (self.orange.pos["current"] == self.pacbot.pos and self.orange.frightened_counter == 0) or
        (self.blue.pos["current"] == self.pacbot.pos and self.blue.frightened_counter == 0))

    def _check_if_ghosts_eaten(self):
        self._check_if_ghost_eaten(self.red)
        self._check_if_ghost_eaten(self.pink)
        self._check_if_ghost_eaten(self.orange)
        self._check_if_ghost_eaten(self.blue)

    def _check_if_ghost_eaten(self, ghost):
        if ghost.pos["current"] == self.pacbot.pos and ghost.frightened_counter > 0:
            ghost.send_home()
            self.score += ghost_score * self.frightened_multiplier
            self.frightened_multiplier += 1

    def _are_all_pellets_eaten(self):
        return self.pellets == 0 and self.power_pellets == 0


    def _is_game_over(self):
        return (self._are_all_pellets_eaten() and
                not (self.red.is_frightened() or
                    self.red.is_frightened() or
                    self.red.is_frightened() or
                    self.red.is_frightened()))

    def _swap_state_if_necessary(self):
        if self.state_counter in state_swap_times:
            if self.state == chase:
                self.state = scatter
            else:
                self.state = chase

    def pause(self):
        self.elapsed_time += time.time() - self.previous_start
        self.play = False

    def unpause(self):
        self.previous_start = time.time()
        self.play = True

    def next_step(self):
        if self._is_game_over():
            self._end_game()
        if self._should_die():
            self._die()
        else:
            self._check_if_ghosts_eaten()
            if self.update_ticks % ticks_per_update == 0:
                self._update_ghosts()
                self._check_if_ghosts_eaten()
                if self.state == frightened:
                    if self.frightened_counter == 1:
                        self._end_frightened()
                    self.frightened_counter -= 1
                else:
                    self._swap_state_if_necessary()
                    self.state_counter += 1
                self.start_counter += 1


            self._update_score()
            self.update_ticks += 1

    def restart(self):
        self.grid = copy.deepcopy(grid)
        self.pellets = sum([col.count(o) for col in self.grid])
        self.power_pellets = sum([col.count(O) for col in self.grid])
        self.old_state = chase
        self.state = scatter
        self.frightened_counter = 0
        self.frightened_multiplier = 1
        self._respawn_agents()
        self.score = 0
        self.play = False
        self.start_counter = 0
        self.state_counter = 0
        self.update_ticks = 0
        self.lives = starting_lives
        self.elapsed_time = 0
        self._update_score()
