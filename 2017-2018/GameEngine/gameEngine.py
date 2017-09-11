from gameState import *
from threading import Thread, Timer
from variables import *
from terminalPrinter import *
import time
from stateConverter import *

input_signal = sig_normal
game = GameState()
state_buffer = StateConverter.convert_game_state_to_proto(game)

def run_game():
    global game, input_signal, state_buffer
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
            state_buffer = StateConverter.convert_game_state_to_proto(game)
        time.sleep(1.0/game_frequency)

def update_pacbot_pos():
    global game
    return
    #TODO: Add logic for getting pacbot position and direction from the computer vision plugin

def main():
    global game, input_signal, state_buffer

    Thread(target = run_game).start()

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

if __name__ == "__main__":
    main()
