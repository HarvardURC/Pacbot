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
        self.pos = { 'current' : (x1,y1), 'next' : (x2,y2)}
        self.direction = direction
        self.scared_counter = 8
        self.homed = False
        self.switched = False
        self.switched_pos = None
     
    def respawn(self, x1, y1, x2, y2, color,direction):
        self.color = color
        self.pos = { 'current' : (x1,y1), 'next' : (x2,y2)}
        self.direction = direction
        self.scared_counter = 8
        

    def dehome(self):
        self.homed = False

    def switch(self,pos):
        self.switched_pos = pos
        self.switched = True

    def update(self,tuple):
        if self.switched :
            self.pos["graph"] = self.switched_pos
            self.homed = True
            self.switched = False
        self.pos['current'] = self.pos['next']
        self.pos['next'] = tuple[0]
        self.direction = tuple[1]

    def send_home(self):
        self.pos['current'] = (15,12)
        self.pos['next'] = (14,12)
        self.pos['graph'] = (12, 15)
        self.direction = up
        self.scared_counter = 0
        self.homed = True

    def getDirection(self):
        self.direction

    def getPosition(self):
        return (self.pos['current'][1], 30 - self.pos['current'][0])


class AgentState:
  """
  AgentStates hold the state of an agent (configuration, speed, scared, etc).
  """

  def __init__( self, startConfiguration):
    self.start = startConfiguration
    self.configuration = startConfiguration
  
  def getPosition(self):
    return self.configuration.getPosition()

  def getDirection(self):
    return self.configuration.getDirection()


class GameState:
    def __init__(self, grid, layout,pacbot):
        self.game_on = True
        self.lives = 3
        self.state = scatter
        self.score = 0
        self.counter = 0
        self.start_counter = 0
        self.grid = grid
        self.frightened_counter = 0
        # self.scatter_timer = 0
        self.frightened_eaten = 1
        self.scattered = False
        self.food = layout.food.copy()
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.play = False
        self.respawn = False


        self.agentStates = []

        self.pacbot = pacbot

        self.agentStates.append(Configuration(11,13,11,12, 'red',left))
        self.agentStates.append(Configuration(15,14,14,14, 'pink',up))
        self.agentStates.append(Configuration(15,15,14,15,'orange',up))
        self.agentStates.append(Configuration(15,12,14,12,'blue',up))

        self.red = self.agentStates[0]
        self.pink = self.agentStates[1]
        self.orange = self.agentStates[2]
        self.blue = self.agentStates[3]

        self.gstate = {'foodEaten' : [], 'layout' : self.layout, 'agentStates' : self.agentStates,
                        'respawn' : False, 
                        'capsuleEaten' : [],
                        'scared' : False,
                        'scatter': False,
                        'score' : self.score,
                        'lives' : self.lives}

    def change_state(self,state):
        if state == scatter:
            self.scattered = True
        elif state == frightened:
            self.frightened_counter = 13
            self.scattered = True

        self.state = state

    def update_ghosts(self):
        if self.red.scared_counter < 8:
            self.red.update(scared_path[self.red.scared_counter])
            self.red.scared_counter += 1
        else:
            self.red.update(next_move(self.pacbot,self.red,self.grid,self.state, scattered = self.scattered))
        if self.start_counter < 3:
            self.pink.update(pink_path[self.start_counter])
        elif self.pink.scared_counter < 8:
            self.pink.update(scared_path[self.pink.scared_counter])
            self.pink.scared_counter += 1
        else:
            self.pink.update(next_move(self.pacbot,self.pink,self.grid,self.state, scattered = self.scattered))
        if self.start_counter < 40:
            self.orange.update(orange_path[self.start_counter])
        elif self.orange.scared_counter < 8:
            self.orange.update(scared_path[self.orange.scared_counter])
            self.orange.scared_counter += 1
        else:
            self.orange.update(next_move(self.pacbot,self.orange,self.grid,self.state,scattered = self.scattered))
        if self.start_counter < 24:
            self.blue.update(blue_path[self.start_counter])
        elif self.blue.scared_counter < 8:
            self.blue.update(scared_path[self.blue.scared_counter])
            self.blue.scared_counter += 1
        else:
            self.blue.update(next_move(self.pacbot,self.blue,self.grid,self.state,self.red,scattered = self.scattered))

    def update_score(self, pacbot = None):
        
        if pacbot != None:
            if self.grid[pacbot.pos[0]][pacbot.pos[1]] == o:
                self.gstate['foodEaten'].append((pacbot.pos[1] , 30 - pacbot.pos[0]))
                self.grid[pacbot.pos[0]][pacbot.pos[1]] = e
                self.score += 10
        
            
            if self.grid[pacbot.pos[0]][pacbot.pos[1]] == O:
                self.grid[pacbot.pos[0]][self.pacbot.pos[1]] = e
                self.score += 50
                self.gstate['capsuleEaten'].append((pacbot.pos[1] , 30 - pacbot.pos[0]))
                self.change_state(frightened)
                self.gstate['scared'] = True
        else:

            if self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == o:
                self.gstate['foodEaten'].append((self.pacbot.pos[1] , 30 - self.pacbot.pos[0]))
                self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
                self.score += 10

                
            if self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] == O:
                self.grid[self.pacbot.pos[0]][self.pacbot.pos[1]] = e
                self.score += 50
                self.gstate['capsuleEaten'].append((self.pacbot.pos[1] , 30 - self.pacbot.pos[0]))
                self.change_state(frightened)
                self.gstate['scared'] = True

 
    def despawn(self):
        self.gstate["respawn"] = False


    def game_go(self, pacbot, fast = True):
        if not fast:
            self.update_ghosts()

        self.pacbot = pacbot

        # clean_screen(33)
        # display_game(self.pacbot,self.red,self.pink,self.orange,self.blue,self.score,self.lives,self.state,self.grid)
 
        if self.game_on:
            # update ghost positions
            if self.state == scatter:
                # if self.scatter_counter == 1:
                #     self.change_state(chase)
                if not fast:
                    if self.scattered:
                        self.scattered = not self.scattered

                # if not fast:
                #     self.scatter_counter -= 1

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
                        self.gstate["respawn"] = True
                        self.lives -= 1
                        self.update_score()
                        self.play = False
                        self.respawn = True

                    else:
                        self.play = False
                        self.respawn = True
                        print("Success: " + str(self.score) )
                        self.game_on = False
                
                else:
                    self.update_score()

                    if not fast:
                        if self.counter == 20:
                            self.change_state(chase)

                        elif self.counter == 80:
                            self.change_state(scatter)

                        elif self.counter == 100:
                            self.change_state(chase)

                        elif self.counter == 160:
                            self.change_state(scatter)

                        elif self.counter == 180:
                            self.change_state(chase)

                        elif self.counter == 240:
                            self.change_state(scatter)

                        elif self.counter == 260:
                            self.change_state(chase)
                if not fast:
                    self.counter += 1

            elif self.state == frightened:
                if not fast:
                    if self.scattered:
                        self.scattered = not self.scattered

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
                    self.gstate['scared'] = False
                
                if not fast:
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
                        self.gstate["respawn"] = True
                        self.start_counter = 0 
                        self.lives -= 1
                        self.update_score()
                        self.play = False
                        self.respawn = True

                    else:
                        self.play = False
                        self.respawn = True
                        print("Success: " + str(self.score) )
                        self.game_on = False
                
                else:
                    if not fast:
                        if self.counter == 20:
                            self.change_state(chase)

                        elif self.counter == 80:
                            self.change_state(scatter)

                        elif self.counter == 100:
                            self.change_state(chase)

                        elif self.counter == 160:
                            self.change_state(scatter)

                        elif self.counter == 180:
                            self.change_state(chase)

                        elif self.counter == 240:
                            self.change_state(scatter)

                        elif self.counter == 260:
                            self.change_state(chase)



                self.update_score()
                
                if not fast:
                    self.counter += 1

        if not fast:
            self.start_counter += 1

        self.gstate["score"] = self.score
        self.gstate["lives"] = self.lives

