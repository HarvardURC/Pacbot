#High Level Game code for PacGhosts
from gameState import *
from threading import Thread, Timer
from variables import *
import time

input_signal = sig_normal
game = GameState()

def handleInput():
    global game, input_signal

    while True:
        line = sys.stdin.readline()
        print(line)
        if line.strip() == 'r' :
            game.play = False
            input_signal = sig_restart

        elif line.strip() == 'p' :
            game.play = not game.play

        elif line.strip() == 'q' :
            input_signal = sig_quit
            cleanup_stop_thread()
            sys.exit()

        time.sleep(0.2)
        sys.stdout.flush()

def update_pacbot_pos():
    global game
    #TODO: Add logic for getting pacbot position and direction from the computer vision plugin

def main():
    global game, input_signal

    Thread(target = handleInput).start()

    while True:
        if input_signal == sig_quit:
            cleanup_stop_thread()
            sys.exit()
        if input_signal == sig_restart:
            game.restart()
            input_signal = sig_normal
        elif game.play:
            update_pacbot_pos()
            game.next_step()
        time.sleep(1.0/game_frequency)

if __name__ == "__main__":
    main()
