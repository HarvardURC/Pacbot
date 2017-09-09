from graphicsUtils import *        
import math, time
import copy

###########################
#  GRAPHICS DISPLAY CODE  #
###########################

# Most code by Dan Klein and John Denero written or rewritten for cs188, UC Berkeley.
# Some code from a Pacman implementation by LiveWires, and used / modified with permission.

FRAME_TIME=0.000001 # The time that pacman's animation last
PAUSE_TIME= 0   # Pause time between frames
DEFAULT_GRID_SIZE = 30
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(0,0,0)    
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 255.0/255.0)
INFO_PANE_COLOR = formatColor(.4,.4,0)
SCORE_COLOR = formatColor(.9, .9, .9)

GHOST_COLORS = []  
GHOST_COLORS.append(formatColor(221.0/255.0,0,0)) 
GHOST_COLORS.append(formatColor(234.0/255.0,130.0/255.0,229.0/255.0)) 
GHOST_COLORS.append(formatColor(255.0/255.0,150.0/255.0,0))
GHOST_COLORS.append(formatColor(70.0/255.0,191.0/255.0,238.0/255.0))  


GHOST_SHAPE = [                
    ( 0,    0.3 ),            
    ( 0.25, 0.75 ),           
    ( 0.5,  0.3 ),
    ( 0.75, 0.75 ),
    ( 0.75, -0.5 ),
    ( 0.5,  -0.75 ),
    (-0.5,  -0.75 ),
    (-0.75, -0.5 ),
    (-0.75, 0.75 ),
    (-0.5,  0.3 ),
    (-0.25, 0.75 )
  ]
GHOST_SIZE = 0.65
SCARED_COLOR = formatColor(1,1,1)    

GHOST_VEC_COLORS = map(colorToVector, GHOST_COLORS)   

# Food
FOOD_COLOR = formatColor(1,1,1)     
FOOD_SIZE = 0.1   

# Laser
LASER_COLOR = formatColor(1,0,0)     
LASER_SIZE = 0.02   
        
# Capsule graphics
CAPSULE_COLOR = formatColor(1,1,1)
CAPSULE_SIZE = 0.25 

# Drawing walls
WALL_RADIUS = 0.15

class InfoPane:
  def __init__(self, layout, gridSize, zoom):
    self.gridSize = gridSize
    self.width = (layout.width) * gridSize
    self.base = (layout.height + 1) * gridSize
    self.height = INFO_PANE_HEIGHT 
    self.drawPane(zoom)

  def toScreen(self, pos, y = None):
    """
      Translates a point relative from the bottom left of the info pane.
    """
    if y == None:
      x,y = pos
    else:
      x = pos
      
    x = self.gridSize + x # Margin
    y = self.base + y 
    return x,y

  def drawPane(self, zoom):
    color = formatColor(1,1,1)     
    size = int(25/.95 * zoom)
    self.scoreText = text( self.toScreen(30/.95 * zoom, -415/.95*zoom), color, "SCORE:    \n    0", "Joystix", size, "bold")
    self.livesText = text( self.toScreen(630/.95 * zoom, -415/.95 * zoom), color, "LIVES:    \n    3", "Joystix", size, "bold")
    
  def updateScore(self, score, lives):
    changeText(self.scoreText, "SCORE:    \n %4d" % score)
    changeText(self.livesText, "LIVES:    \n %4d" % lives)

  

class PacmanGraphics:
    def __init__(self, zoom=1.0):  
        self.have_window = 0
        self.currentGhostImages = {}
        self.zoom = zoom
        self.gridSize = DEFAULT_GRID_SIZE * zoom

    def initialize(self, state):
        self.startGraphics(state)
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

    def startGraphics(self, state):
        self.layout = state['layout']
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize, self.zoom)
        self.currentState = layout

    def drawStaticObjects(self, state):
        layout = self.layout
        # self.drawWalls(layout.walls)
        self.food = self.drawFood(layout.food)
        self.capsules = self.drawCapsules(layout.capsules)
        refresh

    def drawAgentObjects(self, state):
        self.agentImages = [] # (agentState, image)
        copyState = copy.deepcopy(state['agentStates'])
        for index, agent in enumerate(state['agentStates']):
          # if agent.isPacman:
          #   image = self.drawPacman(agent, index)
          #   self.agentImages.append( (agent, image) )
          # else:  

            image = self.drawGhost(agent, index, state['scared'])
            self.agentImages.append( (copyState[index], image) )
        refresh

    def update(self, newState):
        if newState['respawn']:
          for agentIndex in range(4):
                agentState = newState['agentStates'][agentIndex]
                copyState = copy.deepcopy(newState['agentStates'])

                prevState, prevImage = self.agentImages[agentIndex]

                self.moveGhost(agentState, agentIndex, prevState, prevImage, newState["scared"], True)
                self.agentImages[agentIndex] = (copyState[agentIndex], prevImage)
          newState["respawn"] = False
          sleep(5)
        else:
            for agentIndex in range(4):
                agentState = newState['agentStates'][agentIndex]
                copyState = copy.deepcopy(newState['agentStates'])

                prevState, prevImage = self.agentImages[agentIndex]

                self.moveGhost(agentState, agentIndex, prevState, prevImage, newState["scared"], agentState.homed)
                self.agentImages[agentIndex] = (copyState[agentIndex], prevImage)

                if agentState.homed:
                  agentState.dehome()
              
        if newState['foodEaten'] != []:
          for eaten in newState['foodEaten']:
            self.removeFood(eaten, self.food)
          newState['foodEaten'] = []
        if newState['capsuleEaten'] != []:
          for eaten in newState['capsuleEaten']:
            self.removeCapsule(eaten, self.capsules)
          newState['capsuleEaten'] = []
        
        self.infoPane.updateScore(newState["score"], newState["lives"])
                

    def make_window(self, width, height):
        grid_width = (width-1) * self.gridSize 
        grid_height = (height-1) * self.gridSize 
        screen_width = 2*self.gridSize + grid_width
        screen_height = 2*self.gridSize + grid_height 

        begin_graphics(screen_width,    
                       screen_height,
                       BACKGROUND_COLOR,
                       "HURC Pacbot")

    def getEndpoints(self, direction, position=(0,0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi*pos)
        
        delta = width / 2
        if (direction == 'left'):
          endpoints = (180+delta, 180-delta)
        elif (direction == 'up'):
          endpoints = (90+delta, 90-delta)
        elif (direction == 'down'):
          endpoints = (270+delta, 270-delta)
        else:
          endpoints = (0+delta, 0-delta)
        return endpoints

    def getGhostPos(self, ghost):
        # Overridden in FirstPersonGraphics
        return ghost.getPosition()

    def getGhostColor(self, ghost, ghostIndex, scared):
        if scared:
          return SCARED_COLOR
        else:
          return GHOST_COLORS[ghostIndex]

    def drawGhost(self, ghost, agentIndex, scared):
        pos = self.getGhostPos(ghost)
        dir = ghost.direction
        (screen_x, screen_y) = (self.to_screen(pos)) 
        coords = []          
        for (x, y) in GHOST_SHAPE:
          coords.append((x*self.gridSize*GHOST_SIZE + screen_x, y*self.gridSize*GHOST_SIZE + screen_y))

        colour = self.getGhostColor(ghost, agentIndex, scared)
        body = polygon(coords, colour, filled = 1)
        WHITE = formatColor(1.0, 1.0, 1.0)
        BLACK = formatColor(0.0, 0.0, 0.0)
        
        dx = 0
        dy = 0
        if dir == 'up':
          dy = -0.2
        if dir == 'down':
          dy = 0.2
        if dir == 'right':
          dx = 0.2
        if dir == 'left':
          dx = -0.2

        leftEye = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE)
        rightEye = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE)
        leftPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK)
        rightPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK)
        ghostImageParts = []
        ghostImageParts.append(body)
        ghostImageParts.append(leftEye)
        ghostImageParts.append(rightEye)
        ghostImageParts.append(leftPupil)
        ghostImageParts.append(rightPupil)

        return ghostImageParts

    def moveEyes(self, pos, dir, eyes):
        (screen_x, screen_y) = (self.to_screen(pos)) 
        dx = 0
        dy = 0
        if dir == 'up':
          dy = -0.2
        if dir == 'down':
          dy = 0.2
        if dir == 'right':
          dx = 0.2
        if dir == 'left':
          dx = -0.2
        moveCircle(eyes[0],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
        moveCircle(eyes[1],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
        moveCircle(eyes[2],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)
        moveCircle(eyes[3],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)
    
    def moveGhost(self, ghost, ghostIndex, prevGhost, ghostImageParts, scared, respawn):
      if respawn:
        # ghost.change_pos()
        for ghostImagePart in ghostImageParts:
          move_to(ghostImagePart, self.to_screen(self.getGhostPos(ghost)))
        refresh

      else:

        old_x, old_y = self.to_screen(self.getGhostPos(prevGhost))
        # ghost.change_pos()
        new_x, new_y = self.to_screen(self.getGhostPos(ghost))
       
        delta = new_x - old_x, new_y - old_y
        
        for ghostImagePart in ghostImageParts:
          move_by(ghostImagePart, delta)
        refresh
          
      if scared:
        color = SCARED_COLOR
      else:
        color = GHOST_COLORS[ghostIndex]

     
      edit(ghostImageParts[0], ('fill', color), ('outline', color))  
      self.moveEyes(self.getGhostPos(ghost), ghost.direction, ghostImageParts[-4:])
      refresh

    def finish(self):
        end_graphics()
  
    def to_screen(self, point):
        ( x, y ) = point
        #y = self.height - y
        x = (x + 1) * self.gridSize
        y = (self.height - y) * self.gridSize
        return ( x, y )
  
  # Fixes some TK issue with off-center circles
    def to_screen2(self, point):
        ( x, y ) = point
        #y = self.height - y
        x = (x + 1) * self.gridSize
        y = (self.height  - y)*self.gridSize
        return ( x, y )
  
    def drawWalls(self, wallMatrix):
        for xNum, x in enumerate(wallMatrix):
            for yNum, cell in enumerate(x):
                if cell: # There's a wall here
                  pos = (xNum, yNum)
                  screen = self.to_screen(pos)
                  screen2 = self.to_screen2(pos)
                  
                  # draw each quadrant of the square based on adjacent walls
                  wIsWall = self.isWall(xNum-1, yNum, wallMatrix)
                  eIsWall = self.isWall(xNum+1, yNum, wallMatrix)
                  nIsWall = self.isWall(xNum, yNum+1, wallMatrix)
                  sIsWall = self.isWall(xNum, yNum-1, wallMatrix)
                  nwIsWall = self.isWall(xNum-1, yNum+1, wallMatrix)
                  swIsWall = self.isWall(xNum-1, yNum-1, wallMatrix)
                  neIsWall = self.isWall(xNum+1, yNum+1, wallMatrix)
                  seIsWall = self.isWall(xNum+1, yNum-1, wallMatrix)
                  
                  # NE quadrant
                  if (not nIsWall) and (not eIsWall):
                    # inner circle
                    circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (0,91), 'arc')
                  if (nIsWall) and (not eIsWall):
                    # vertical line
                    line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5)-1)), WALL_COLOR)
                  if (not nIsWall) and (eIsWall):
                    # horizontal line
                    line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                  if (nIsWall) and (eIsWall) and (not neIsWall):
                    # outer circle
                    circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (180,271), 'arc')
                    line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                    line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5))), WALL_COLOR)
                  
                  # NW quadrant
                  if (not nIsWall) and (not wIsWall):
                    # inner circle
                    circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (90,181), 'arc')
                  if (nIsWall) and (not wIsWall):
                    # vertical line
                    line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5)-1)), WALL_COLOR)
                  if (not nIsWall) and (wIsWall):
                    # horizontal line
                    line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                  if (nIsWall) and (wIsWall) and (not nwIsWall):
                    # outer circle
                    circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (270,361), 'arc')
                    line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(-1)*WALL_RADIUS)), WALL_COLOR)
                    line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5))), WALL_COLOR)
                  
                  # SE quadrant
                  if (not sIsWall) and (not eIsWall):
                    # inner circle
                    circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (270,361), 'arc')
                  if (sIsWall) and (not eIsWall):
                    # vertical line
                    line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5)+1)), WALL_COLOR)
                  if (not sIsWall) and (eIsWall):
                    # horizontal line
                    line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                  if (sIsWall) and (eIsWall) and (not seIsWall):
                    # outer circle
                    circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (90,181), 'arc')
                    line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                    line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5))), WALL_COLOR)
                  
                  # SW quadrant
                  if (not sIsWall) and (not wIsWall):
                    # inner circle
                    circle(screen2, WALL_RADIUS * self.gridSize, WALL_COLOR, 0, (180,271), 'arc')
                  if (sIsWall) and (not wIsWall):
                    # vertical line
                    line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5)+1)), WALL_COLOR)
                  if (not sIsWall) and (wIsWall):
                    # horizontal line
                    line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                  if (sIsWall) and (wIsWall) and (not swIsWall):
                    # outer circle
                    circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, WALL_COLOR, 0, (0,91), 'arc')
                    line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(1)*WALL_RADIUS)), WALL_COLOR)
                    line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5))), WALL_COLOR)
                  
    def isWall(self, x, y, walls):
        if x < 0 or y < 0:
          return False
        if x >= walls.width or y >= walls.height:
          return False
        return walls[x][y]
      
    def drawFood(self, foodMatrix ):
        foodImages = []
        for xNum, x in enumerate(foodMatrix):
          imageRow = []
          foodImages.append(imageRow)
          for yNum, cell in enumerate(x):
            if cell: # There's food here
              screen = self.to_screen((xNum, yNum ))
              dot = circle( screen, 
                            FOOD_SIZE * self.gridSize, 
                            color = FOOD_COLOR, 
                            filled = 1,
                            width = 1)
              imageRow.append(dot)
            else:
              imageRow.append(None)
        return foodImages
      
    def drawCapsules(self, capsules ):
        capsuleImages = {}
        for capsule in capsules:
          ( screen_x, screen_y ) = self.to_screen(capsule)
          dot = circle( (screen_x, screen_y), 
                            CAPSULE_SIZE * self.gridSize, 
                            color = CAPSULE_COLOR, 
                            filled = 1,
                            width = 1)
          capsuleImages[capsule] = dot
        return capsuleImages
      
    def removeFood(self, cell, foodImages ):
        x, y = cell
        remove_from_screen(foodImages[x][y])
        
    def removeCapsule(self, cell, capsuleImages ):
        x, y = cell
        remove_from_screen(capsuleImages[(x, y)])

def add(x, y):
  return (x[0] + y[0], x[1] + y[1]) 







