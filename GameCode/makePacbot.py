class PacBot:
    """
        Allows initializing and updating information about PacBot
    """
    def __init__(self, pacbot_pos, pacbot_direction):
    	self.pos = pacbot_pos
        self.direction = pacbot_direction
        
    def update(self,position, direction):
    	if position[0] != -1 and position[1] != -1:
        	self.pos = position
        	self.direction = direction
        else:
        	pass