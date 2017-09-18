from .variables import *

class PacBot:
    """
        Allows initializing and updating information about PacBot
    """
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.pos = pacbot_starting_pos
        self.direction = pacbot_starting_dir

    def update(self,position, direction):
        if position[0] <= 27 and position[0] >= 0 and position[1] <= 30 and position[1] >= 0:
            self.pos = position
            self.direction = direction
        else:
            pass
