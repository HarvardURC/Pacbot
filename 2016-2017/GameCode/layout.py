
import os
import random

VISIBILITY_MATRIX_CACHE = {}

def manhattanDistance( xy1, xy2 ):
  """
  Returns the Manhattan distance between points xy1 and xy2
  """
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

class Grid:
  """
  A 2-dimensional array of objects backed by a list of lists.  Data is accessed
  via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
  y vertical and the origin (0,0) in the bottom left corner.  
  
  The __str__ method constructs an output that is oriented like a pacman board.
  """
  def __init__(self, width, height, initialValue=False):
    if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
    self.width = width
    self.height = height
    self.data = [[initialValue for y in range(height)] for x in range(width)]

  def __getitem__(self, i):
    return self.data[i]
  
  def __setitem__(self, key, item):
    self.data[key] = item
    
  def __str__(self):
    out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
    out.reverse()
    return '\n'.join([''.join(x) for x in out])
  
  def __eq__(self, other):
    if other == None: return False
    return self.data == other.data

  def __hash__(self):
    return hash(str(self))
    base = 1
    h = 0
    for l in self.data:
      for i in l:
        if i:
          h += base
        base *= 2
    return hash(h)
  
  def copy(self):
    g = Grid(self.width, self.height)
    g.data = [x[:] for x in self.data]
    return g
  
  def deepCopy(self):
    return self.copy()
  
  def shallowCopy(self):
    g = Grid(self.width, self.height)
    g.data = self.data
    return g
    
  def count(self, item =True ):
    return sum([x.count(item) for x in self.data])
    
  def asList(self, key = True):
    list = []
    for x in range(self.width):
      for y in range(self.height):
        if self[x][y] == key: list.append( (x,y) )
    return list

class Layout:
  """
  A Layout manages the static information about the game board.
  """
  
  def __init__(self, layoutText):
    self.width = len(layoutText[0])
    self.height= len(layoutText)
    self.walls = Grid(self.width, self.height, False)
    self.food = Grid(self.width, self.height, False)
    self.capsules = []
    self.agentPositions = []
    self.processLayoutText(layoutText)
    self.layoutText = layoutText
    # self.initializeVisibilityMatrix()
    
  def initializeVisibilityMatrix(self):
    global VISIBILITY_MATRIX_CACHE
    if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
      from game import Directions
      vecs = [(-0.5,0), (0.5,0),(0,-0.5),(0,0.5)]
      dirs = [Directions.NORTH, Directions.SOUTH, Directions.WEST, Directions.EAST]
      vis = Grid(self.width, self.height, {Directions.NORTH:set(), Directions.SOUTH:set(), Directions.EAST:set(), Directions.WEST:set(), Directions.STOP:set()})
      for x in range(self.width):
        for y in range(self.height):
          if self.walls[x][y] == False:
            for vec, direction in zip(vecs, dirs):
              dx, dy = vec
              nextx, nexty = x + dx, y + dy
              while (nextx + nexty) != int(nextx) + int(nexty) or not self.walls[int(nextx)][int(nexty)] :
                vis[x][y][direction].add((nextx, nexty))
                nextx, nexty = x + dx, y + dy
      self.visibility = vis      
      VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
    else:
      self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]
      
  def isWall(self, pos):
    x, col = pos
    return self.walls[x][col]
  
  def getRandomLegalPosition(self):
    x = random.choice(range(self.width))
    y = random.choice(range(self.height))
    while self.isWall( (x, y) ):
      x = random.choice(range(self.width))
      y = random.choice(range(self.height))
    return (x,y)
    
  def processLayoutText(self, layoutText):
    """
    Coordinates are flipped from the input format to the (x,y) convention here
    
    The shape of the maze.  Each character  
    represents a different type of object.   
     % - Wall                               
     . - Food
     o - Capsule
     G - Ghost
     P - Pacman
    Other characters are ignored.
    """
    maxY = self.height - 1
    for y in range(self.height):       
      for x in range(self.width):
        layoutChar = layoutText[maxY - y][x]  
        self.processLayoutChar(x, y, layoutChar)
    self.agentPositions.sort()
    self.agentPositions = [ ( i == 0, pos) for i, pos in self.agentPositions]
  
  def processLayoutChar(self, x, y, layoutChar):
    if layoutChar == '%':      
      self.walls[x][y] = True
    elif layoutChar == '.':
      self.food[x][y] = True 
    elif layoutChar == 'o':    
      self.capsules.append((x, y))   
    elif layoutChar == 'P':    
      self.agentPositions.append( (0, (x, y) ) )
    elif layoutChar in ['G']:    
      self.agentPositions.append( (1, (x, y) ) )
    elif layoutChar in  ['1', '2', '3', '4']:
      self.agentPositions.append( (int(layoutChar), (x,y)))

def getLayout(name, back = 2):
  return Layout([line.strip() for line in open(name)])

  