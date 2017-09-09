class AgentState:
    """
    Holds x,y coordinates for each ghost and pacman, along with next position
    for each ghost.
    (0,0) is the lower left.
    """
    def __init__(self, x1, y1, x2, y2, color, direction, start_delay):
        self.color = color
        self.init_direction = direction
        self.init_moves = [x1, y1, x2, y2]
        self.start_delay = start_delay

    def respawn(self):
        self.pos = {
            'current' : (self.init_moves[0], self.init_moves[1]),
            'next' : (self.init_moves[2],self.init_moves[3])
        }
        self.direction = self.init_direction
        self.scared_counter = 8

    def update(self,tuple):
        self.pos['current'] = self.pos['next']
        self.pos['next'] = tuple[0]
        self.direction = tuple[1]

    def send_home(self):
        self.pos['current'] = (15,12)
        self.pos['next'] = (14,12)
        self.pos['graph'] = (12, 15)
        self.direction = up
        self.scared_counter = 0

    def getDirection(self):
        self.direction

    def getPosition(self):
        return (self.pos['current'][1], 30 - self.pos['current'][0])
