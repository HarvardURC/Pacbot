#High Level Game code for PacGhosts
from variables import *
from gameState import *
from display import *
from pacbot import *
import random
from json import dumps
import copy
from threading import Thread, Lock, Timer
import time

restart = False
game = GameState(PacBot((23,13), "right"))

def handleInput():
    global game, restart

    while True:
        line = sys.stdin.readline()
        print(line)
        if line.strip() == 'r' :
            game.play = False
            restart = True

        elif line.strip() == 'p' :
            game.play = not game.play

        elif line.strip() == 'e' :
            cleanup_stop_thread()
            sys.exit()

        time.sleep(1)
        sys.stdout.flush()

def update_pacbot_pos():
    #TODO: Add logic for getting pacbot position and direction from the computer vision plugin

def step_callback():
    global game, restart

    if restart:
        game.restart()
        restart = False
    elif game.play:
        update_pacbot_pos()
        game.next_step()

    #TODO: Add callback to step_callback

def main():
    global game, restart

    Thread(target = handleInput).start()

    #TODO: Add callback to step_callback


if __name__ == "__main__":
    main()
