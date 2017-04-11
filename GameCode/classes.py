from variables import *
from solver import *
from ghostpaths import *
from display import *

class Configuration:
    """
    Holds x,y coordinates for each ghost and pacman, along with next position
    for each ghost. 
    (0,0) is the lower left.
    """
    def __init__(self, x1, y1, x2, y2, color,direction):
        self.color = color
        self.pos = { 'current' : (x1,y1), 'next' : (x2,y2), 'graph' : (y1 , 30 - x1)}
        self.direction = direction
        self.scared_counter = 8
     
    def respawn(self, x1, y1, x2, y2, color,direction):
        self.color = color
        self.pos = { 'current' : (x1,y1), 'next' : (x2,y2)}
        self.direction = direction
        self.scared_counter = 8

    def update(self,tuple):
        self.pos['current'] = self.pos['next']
        self.pos['next'] = tuple[0]
        self.direction = tuple[1]

    def send_home(self):
        self.pos['current'] = (15,12)
        self.pos['next'] = (14,12)
        self.direction = up
        self.scared_counter = 0

    def getDirection(self):
        self.direction

    def getPosition(self):
        return self.pos['graph']

    def change_pos(self):
        (x,y) = self.pos['graph']
        if self.direction == up:
            self.pos['graph'] = (x , y + .5)
        elif self.direction == down:
            self.pos['graph'] = (x , y - .5)
        elif self.direction == left:
            self.pos['graph'] = (x -  .5 , y )
        else:
            self.pos['graph'] = (x + .5 , y )

class AgentState:
  """
  AgentStates hold the state of an agent (configuration, speed, scared, etc).
  """

  def __init__( self, startConfiguration):
    self.start = startConfiguration
    self.configuration = startConfiguration
    self.scaredTimer = startConfiguration.scared_counter
  
  def getPosition(self):
    return self.configuration.getPosition()

  def getDirection(self):
    return self.configuration.getDirection()

       
class PacBot:
    """
        Allows initializing and updating information about PacBot
    """
    def __init__(self, x, y, direction):
        self.direction = direction
        self.pos = (x,y)
        
    def update(self,position, direction):
        self.pos = position
        self.direction = direction

class GameState:
    def __init__(self, grid, layout):
        self.game_on = True
        self.lives = 3
        self.state = chase
        self.score = 0
        self.counter = 0
        self.start_counter = 0
        self.grid = grid
        self.frightened_counter = 0
        self.scatter_counter = 0
        self.frightened_eaten = 1
        self.respawn = False

        self.food = layout.food.copy()
        self.capsules = layout.capsules[:]
        self.layout = layout

        self._foodEaten = None
        self._capsuleEaten = None

        self.agentStates = []

        self.pacbot = PacBot(23,13,left)

        self.agentStates.append(Configuration(11,13,11,12, 'red',left))
        self.agentStates.append(Configuration(15,14,14,14, 'pink',up))
        self.agentStates.append(Configuration(15,15,14,15,'orange',up))
        self.agentStates.append(Configuration(15,12,14,12,'blue',up))

        self.red = self.agentStates[0]
        self.pink = self.agentStates[1]
        self.orange = self.agentStates[2]
        self.blue = self.agentStates[3]

        self.gstate = {'layout' : self.layout, 'agentStates' : self.agentStates,
                        'respawn' : self.respawn, '_foodEaten' : self._foodEaten,
                        '_capsuleEaten' : self._capsuleEaten}

    def change_state(self,state):
        if state == scatter:
            self.scatter_counter = 60
        elif state == frightened:
            self.frightened = 60

        self.state = state

    def update_ghosts(self):
        if self.red.scared_counter < 8:
            self.red.update(scared_path[self.red.scared_counter])
            self.red.scared_counter += 1
        else:
            self.red.update(next_move(self.pacbot,self.red,self.grid,self.state))
        if self.start_counter < 3:
            self.pink.update(pink_path[self.start_counter])
        elif self.pink.scared_counter < 8:
            self.pink.update(scared_path[self.pink.scared_counter])
            self.pink.scared_counter += 1
        else:
            self.pink.update(next_move(self.pacbot,self.pink,self.grid,self.state))
        if self.start_counter < 40:
            self.orange.update(orange_path[self.start_counter])
        elif self.orange.scared_counter < 8:
            self.orange.update(scared_path[self.orange.scared_counter])
            self.orange.scared_counter += 1
        else:
            self.orange.update(next_move(self.pacbot,self.orange,self.grid,self.state))
        if self.start_counter < 24:
            self.blue.update(blue_path[self.start_counter])
        elif self.blue.scared_counter < 8:
            self.blue.update(scared_path[self.blue.scared_counter])
            self.blue.scared_counter += 1
        else:
            self.blue.update(next_move(self.pacbot,self.blue,self.grid,self.state,self.red))

    def update_score(self):
        self.counter += 1
        self.start_counter += 1

        move_pacman(self.pacbot,self.grid)

        if self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == o:
            self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
            self.score += 10
            self._foodEaten = (self.pacbot.pos[1], 30 - self.pacbot.pos[0])
        if self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == O:
            self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
            self.score += 50
            self.change_state(frightened)
            self.frightened_counter = 50
            self._capsuleEaten = (self.pacbot.pos[1] , 30 - self.pacbot.pos[0])



    def game_go(self):
        self._capsuleEaten = None
        self._foodEaten = None
        self.update_ghosts()

        clean_screen(33)
        display_game(self.pacbot,self.red,self.pink,self.orange,self.blue,self.score,self.lives,self.state,self.grid)

        if self.game_on:
            # update ghost positions
            if self.state == scatter:
                if self.scatter_counter == 1:
                    self.state = chase

                self.scatter_counter -= 1

                if (self.red.pos["current"] == self.pacbot.pos or 
                self.pink.pos["current"] == self.pacbot.pos or 
                self.orange.pos["current"] == self.pacbot.pos or 
                self.blue.pos["current"] == self.pacbot.pos):
                
                    if self.lives > 1:
                        self.pacbot.update((23,14),left)
                        self.red.respawn(11,13,11,12, 'red',left)
                        self.pink.respawn(15,14,14,14, 'pink',up)
                        self.orange.respawn(15,15,14,15,'orange',up)
                        self.blue.respawn(15,12,14,12,'blue',up)
                        self.start_counter = 0 
                        self.lives -= 1
                        self.update_score()

                    else:
                        print("Success")
                        self.game_on = False
                
                else:
                    self.update_score()

            elif self.state == frightened:
                if self.red.pos["current"] == self.pacbot.pos:
                    self.red.send_home()
                    self.score += 200 *  self.frightened_eaten
                    self.frightened_eaten += 1

                elif self.blue.pos["current"] == self.pacbot.pos:
                    self.blue.send_home()
                    self.score += 200 *  self.frightened_eaten
                    self.frightened_eaten += 1

                elif self.orange.pos["current"] == self.pacbot.pos:
                    self.orange.send_home()
                    self.score += 200 *  self.frightened_eaten
                    self.frightened_eaten += 1

                elif self.pink.pos["current"] == self.pacbot.pos:
                    self.pink.send_home()
                    self.score += 200 *  self.frightened_eaten
                    self.frightened_eaten += 1
                
                if self.frightened_counter == 1:
                    self.state = chase
                    self.frightened_eaten = 1

                self.frightened_counter -= 1

                self.update_score()
            else:

                if (self.red.pos["current"] == self.pacbot.pos or 
                self.pink.pos["current"] == self.pacbot.pos or 
                self.orange.pos["current"] == self.pacbot.pos or 
                self.blue.pos["current"] == self.pacbot.pos):

                    if self.lives > 1:
                        self.pacbot.update((23,14),left)
                        self.red.respawn(11,13,11,12, 'red',left)
                        self.pink.respawn(15,14,14,14, 'pink',up)
                        self.orange.respawn(15,15,14,15,'orange',up)
                        self.blue.respawn(15,12,14,12,'blue',up)
                        self.start_counter = 0 
                        self.lives -= 1
                        self.update_score()

                    else:
                        print("Success")
                        self.game_on = False
                
                else:
                    self.update_score()

                    
