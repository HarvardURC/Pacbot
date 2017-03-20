#High Level Game code for PacGhosts
from variables import *
from g import *
from classes import *
from display import *

def main():   
    # initialize the game
    game = GameState(grid)
    # display start postions
    display_game(game.pacbot,game.red,game.pink,game.orange,game.blue,game.score,game.lives,game.state,game.grid)
    move_pacman(game.pacbot,game.grid)

    if game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] == o:
        game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] = e
        game.score += 1
        
    while game.game_on:
        game.game_go()

                        
if __name__ == "__main__":
    main()