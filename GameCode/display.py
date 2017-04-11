from __future__ import print_function
import sys


scatter = "Scatter"
chase = "Chase"
frightened = "Frightened"

I = "Wall"
o = "Food"
e = "No_Food"
O = "Boost"
n = "Home"


def clean_screen(rows):
    """
        cleans rows number of rows from the stdout
    """
    for row in range(rows):
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K")

def display_game(pacbot,red_ghost,pink_ghost,orange_ghost,blue_ghost,score,lives,state,grid):
    """
        Prints the game board with the characters in their current positions
    """
    print("Pacman  Score: " + str(score) + "  State: " + str(state) + "  Lives: " + str(lives))
    for row in range(31):
        for col in range(28):
            if lives == 1:
                

                if state == frightened:
                    if (row,col) == pacbot.pos:
                        print(("P"),end='')
                    elif (row,col) == red_ghost.pos["current"] or (row,col) == pink_ghost.pos["current"] or (row,col) == orange_ghost.pos["current"] or (row,col) == blue_ghost.pos["current"]: 
                        print(("G"),end='')
                    elif grid[row][col] == o:
                        print(".",end='')
                    elif grid[row][col] == O:
                        print(("o"),end='')
                    elif grid[row][col] == e or grid[row][col] == n:
                        print(" ",end='')
                    elif grid[row][col] == I:
                        print("0",end='')
                else:
                    if (row,col) == pacbot.pos and (row,col) == red_ghost.pos["current"]:
                        print("!",end='')
                    elif (row,col) == pacbot.pos and (row,col) == pink_ghost.pos["current"]:
                        print("!",end='')
                    elif (row,col) == pacbot.pos and (row,col) == orange_ghost.pos["current"]:
                        print("!",end='')
                    elif (row,col) == pacbot.pos and (row,col) == blue_ghost.pos["current"]:
                        print("!",end='')
                    elif (row,col) == pacbot.pos:
                        print(("P"),end='')
                    elif (row,col) == red_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == pink_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == orange_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == blue_ghost.pos["current"]:
                        print(("G"),end='')
                    elif grid[row][col] == o:
                        print(".",end='')
                    elif grid[row][col] == O:
                        print(("o"),end='')
                    elif grid[row][col] == e or grid[row][col] == n:
                        print(" ",end='')
                    elif grid[row][col] == I:
                        print("0",end='')
            else:
                if state == frightened:
                    if (row,col) == pacbot.pos:
                        print(("P"),end='')
                    elif (row,col) == red_ghost.pos["current"] or (row,col) == pink_ghost.pos["current"] or (row,col) == orange_ghost.pos["current"] or (row,col) == blue_ghost.pos["current"]: 
                        print(("G"),end='')
                    elif grid[row][col] == o:
                        print(".",end='')
                    elif grid[row][col] == O:
                        print(("o"),end='')
                    elif grid[row][col] == e or grid[row][col] == n:
                        print(" ",end='')
                    elif grid[row][col] == I:
                        print("0",end='')
                else:
                    if (row,col) == pacbot.pos:
                        print(("P"),end='')
                    elif (row,col) == red_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == pink_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == orange_ghost.pos["current"]:
                        print(("G"),end='')
                    elif (row,col) == blue_ghost.pos["current"]:
                        print(("G"),end='')
                    elif grid[row][col] == o:
                        print(".",end='')
                    elif grid[row][col] == O:
                        print(("o"),end='')
                    elif grid[row][col] == e or grid[row][col] == n:
                        print(" ",end='')
                    elif grid[row][col] == I:
                        print("0",end='')

        print()
    print()
    