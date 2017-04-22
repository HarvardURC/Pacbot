import math
from variables import *
import random
import sys
import tty, termios
import signal
    

def find_possible(ghost, pos,direction,grid):
    """
        Finds and returns all possible tiles that the ghost can move to as a list of tuples
    """
    global I, e, o, n
    (x,y) = pos["next"]
    possible=[]
    if pos["next"] == (14,27) and direction == left:
        possible.append((14,26))    
    elif pos["next"] == (14,0) and direction == right:
        possible.append((14,1)) 

    else:
        if (x+1,y) != pos["current"] and grid[x+1][y] != I and grid[x+1][y] != n:
            possible.append((x+1,y))
        if (x-1,y) != pos["current"] and grid[x-1][y] != I and grid[x-1][y] != n:
            possible.append((x-1,y))
        if (x,y+1) != pos["current"] and grid[x][y+1] != I and grid[x][y+1] != n:
            possible.append((x,y+1))
        if (x,y-1) != pos["current"] and grid[x][y-1] != I and grid[x][y-1] != n:
            possible.append((x,y-1))
        if possible == []:
            possible.append(pos["current"])
    return possible  
    
def get_direction (pos_prev,pos_new,direction):
    if pos_new[0] > pos_prev[0]:
        return down
    elif pos_new[0] < pos_prev[0]:
        return up
    elif pos_new[1] > pos_prev[1]:
        return right
    elif pos_new[1] < pos_prev[1]:
        return left
    else:
        return direction

def next_move(pacbot, ghost,grid,state,red_ghost=None,scattered = False):
    """
        Finds and returns the possible tile with the shortest distance to the target as a tuple
    """

    if ghost.pos["next"] == (14,0) and ghost.direction == left:
        ghost.switch((28 ,16))
        return (14,27), left


    elif ghost.pos["next"] == (14,27) and ghost.direction == right:
        ghost.switch((-1,16))
        return (14,0), right


    else:
        possible = find_possible(ghost, ghost.pos,ghost.direction,grid)
        third = None
        index = 0
        distances = []

        

        if state == chase:
            if ghost.color == "blue":
                if pacbot.direction == up:
                    x = red_ghost.pos["current"][0] + 2* (pacbot.pos[0]-2 - red_ghost.pos["current"][0])
                    y = red_ghost.pos["current"][1] + 2* (pacbot.pos[1] - red_ghost.pos["current"][1])
                elif pacbot.direction == down:
                    x = red_ghost.pos["current"][0] + 2* (pacbot.pos[0]+2 - red_ghost.pos["current"][0])
                    y = red_ghost.pos["current"][1] + 2* (pacbot.pos[1] - red_ghost.pos["current"][1])
                elif pacbot.direction == left:
                    x = red_ghost.pos["current"][0] + 2* (pacbot.pos[0] - red_ghost.pos["current"][0])
                    y = red_ghost.pos["current"][1] + 2* (pacbot.pos[1]-2 - red_ghost.pos["current"][1])
                elif pacbot.direction == right:
                    x = red_ghost.pos["current"][0] + 2* (pacbot.pos[0] - red_ghost.pos["current"][0])
                    y = red_ghost.pos["current"][1] + 2* (pacbot.pos[1]+2 - red_ghost.pos["current"][1])
                for value in possible:
                    distances.append(distance((x,y),value))
                (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))
                    
            elif ghost.color == "pink":
                if pacbot.direction == up:
                    x = pacbot.pos[0] - 4
                    y = pacbot.pos[1]
                elif pacbot.direction == down:
                    x = pacbot.pos[0] + 4
                    y = pacbot.pos[1]
                elif pacbot.direction == left:
                    x = pacbot.pos[0]
                    y = pacbot.pos[1] - 4
                elif pacbot.direction == right:
                    x = pacbot.pos[0]
                    y = pacbot.pos[1] + 4
                for value in possible:
                    distances.append(distance((x,y),value))
                (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))
            
            else:  
                for value in possible:
                    distances.append(distance(pacbot.pos,value))
                (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))
                
                if ghost.color == "orange" and min_distance < 8:
                    distances = []
                    for value in possible:
                        distances.append(distance((35,3),value))
                    (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))
            
            third = possible[index]
            
            return third, get_direction(ghost.pos["next"],third,ghost.direction)

        elif state == scatter:
            if scattered:
                return ghost.pos["current"], get_direction(ghost.pos["next"],ghost.pos["current"],ghost.direction)


            else:
                if ghost.color == "red":
                    (x,y) = (-2, 25)
                elif ghost.color == "pink":
                    (x,y) = (-2, 2)
                elif ghost.color == "blue":
                    (x,y) = (31, 27)
                else:
                    (x,y) = (31, 0)

                for value in possible:
                    distances.append(distance((x,y),value))
                (min_distance,index) = min((min_distance,index) for (index,min_distance) in enumerate(distances))
                        
                third = possible[index]

                return third, get_direction(ghost.pos["next"],third,ghost.direction)

        elif state == frightened:
            if scattered:
                return ghost.pos["current"], get_direction(ghost.pos["next"],ghost.pos["current"],ghost.direction)

            else:
                rand_index = random.randint(0, len(possible) - 1)
                third = possible[rand_index]
                return third, get_direction(ghost.pos["next"],third,ghost.direction)

    
    
def distance(pacbot_pos, ghost_pos):
    """ 
        Returns the euclidean distance between two tiles enteres as tuples
    """
    return math.hypot(int(pacbot_pos[0])-int(ghost_pos[0]),int(pacbot_pos[1])-int(ghost_pos[1]))