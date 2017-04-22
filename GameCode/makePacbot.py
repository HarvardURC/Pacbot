class PacBot:
    """
        Allows initializing and updating information about PacBot
    """
    def __init__(self, pacbot_pos, pacbot_direction):
    	self.pos = pacbot_pos
        self.direction = pacbot_direction
        
    def update(self,position, direction):
    	if position[0] <= 30 and position[0] >= 0 and position[1] <= 27 and position[1] >= 0:
        	self.pos = position
        	self.direction = direction
        else:
        	pass