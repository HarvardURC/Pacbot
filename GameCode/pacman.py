#High Level Game code for PacGhosts
from variables import *
from g import *
from classes import *
from display import *
import layout
from graphicsDisplay import *
from BotTracker import *

def main():   
    # initialize the game
    lay = layout.getLayout("pacbotLayout.lay")
    game = GameState(grid, lay)
    graphics = PacmanGraphics(.5)
    graphics.initialize(game.gstate)

    # display start postions
    display_game(game.pacbot,game.red,game.pink,game.orange,game.blue,game.score,game.lives,game.state,game.grid)
    move_pacman(game.pacbot,game.grid)

    if game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] == o:
        game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] = e
        game.score += 1
        
    counter = 1
    while game.game_on:
        # if counter < 2:
        #     graphics.update(game.gstate)
        #     counter += 1
        # else:
        #     counter = 1
        graphics.update(game.gstate)
        game.game_go()
        


                        
if __name__ == "__main__":
    main()