#High Level Game code for PacGhosts
from variables import *
from g import *
from classes import *
from display import *
import layout
from graphicsDisplay import *
from BotTracker import *
from makePacbot import *
import random
from flask import Flask, jsonify
from serial import Serial 
from json import dumps
import copy
from threading import Thread, Lock, Timer
import time
lock = Lock()

restart = False
lay = layout.getLayout("pacbotLayout.lay")
pacbot = PacBot((23,13), "right")
game = GameState(copy.deepcopy(grid), lay, pacbot)
botTracker = BotTracker()
graphics = None
session = True



app = Flask("Pacman")

@app.route('/pac-bot')
def pacBot():
    return jsonify(getFormattedGameData())

def getFormattedGameData():
    if game.play:
        response = {}
        response['pacbot'] = {
            'x': game.pacbot.pos[0],
            'y': game.pacbot.pos[1]
        }
        response['blinky'] = {
            'x': game.red.pos['current'][0],
            'y': game.red.pos['current'][1]
        }
        response['pinky'] = {
            'x': game.pink.pos['current'][0],
            'y': game.pink.pos['current'][1]
        }
        response['clyde'] = {
            'x': game.orange.pos['current'][0],
            'y': game.orange.pos['current'][1]
        }
        response['inky'] = {
            'x': game.blue.pos['current'][0],
            'y': game.blue.pos['current'][1]
        }
        if (game.state == frightened):
            response['specialTimer'] = game.frightened_counter * 0.77
        return response
    else:
        return {'stop': True}

def xBee():
    xbee = Serial('/dev/cu.usbserial-00002014', 9600)
    if (game.game_on):
        m = "$" + string(game.pacbot.pos[0]) + "#" + string(game.pacbot.pos[1]) + "#" 
        m = m + string(game.red.pos[0]) + "#" +string(game.red.pos[1]) + "#" 
        m = m + string(game.pink.pos[0]) + "#" +string(game.pink.pos[1]) + "#" 
        m = m + string(game.blue.pos[0]) + "#" +string(game.blue.pos[1]) + "#"
        if (game.state == frightened):
            m = m + string(int(game.frightened_counter * 0.77))
    else:
        m = "s"
    while True:
        try:
            xbee.write(m)
        # Can add in sleep timer if needed
        except KeyboardInterrupt:
            break
    xbee.halt
    xbee.close()

def main():
    global lay, pacbot, game, botTracker, graphics
    graphics = PacmanGraphics(0.95)

    graphics.initialize(game.gstate)
    graphics.update(game.gstate)

    
    position = botTracker.get_bot_location()
    direction = botTracker.get_bot_direction()
    pacbot.update(position, direction)
    # times = Timer(100.0, scatter_on)
    # scatter_on()
    Thread(target = handleInput).start()
    Thread(target = appRunner).start()
    #Thread(target = xBee).start()
    Thread(target = trackerUpdate).start()
    Thread(target = gameUpdate(graphics)).start()
    

def appRunner():
    app.run(host="0.0.0.0", port=8080)
    
def trackerUpdate():
    global game, play
    while session:
        if game.play: 
            try:
                lock.acquire()
                
                try:
                    position = botTracker.get_bot_location()
                    direction = botTracker.get_bot_direction()
                    pacbot.update(position, direction)
                    game.game_go(pacbot)
                finally:
                    lock.release()
                time.sleep(.05)
            except KeyboardInterrupt:
                break
                


def gameUpdate(graphics):
    global game , play, pacbot, lay  , restart
    # display start postions
    # display_game(game.pacbot,game.red,game.pink,game.orange,game.blue,game.score,game.lives,game.state,game.grid)
    
    if game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] == o:
        game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] = e
        game.score += 10
    

    while session:
        if game.respawn:
            mode_changed = True
            while mode_changed:
                lock.acquire()
                try:   
                    game.respawn = False
                    mode_changed = False
                finally:
                    lock.release()
            
            graphics.update(game.gstate)
            # scatter_no = 0
            # scatter_on()

        if game.play:
            position = botTracker.get_bot_location()
            direction = botTracker.get_bot_direction()


            lock.acquire()
            try:   
                pacbot.update(position, direction)
                game.game_go(pacbot, False)
            finally:
                lock.release()
            graphics.update(game.gstate)

        elif restart:
            restart = False

            mode_changed = True
            while mode_changed:
                lock.acquire()
                try:   
                    lay = layout.getLayout("pacbotLayout.lay")
                    pacbot = PacBot((23,13), "right")
                    game = GameState(copy.deepcopy(grid), lay, pacbot)

                    graphics = PacmanGraphics(0.95)
                    graphics.initialize(game.gstate)
                    graphics.update(game.gstate)
                    mode_changed = False
                finally:
                    lock.release()
            
            # scatter_no = 0
            # scatter_on()

def handleInput():
    global game, pacbot, lay, play, restart
    while session:
        
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

# def scatter_on():
#     global game, scatter_no, times
#     mode_changed = True
#     while mode_changed:
#         lock.acquire()
#         try:   
#             game.state = scatter
#             mode_changed = False
#             scatter_no += 1
#         finally:
#             lock.release()
#     times.cancel()
#     times = Timer(15.0, scatter_off)
#     times.start()
#     print("scatter")
    

# def scatter_off():
#     global game, scatter_no, times
#     mode_changed = True
#     while mode_changed:
#         lock.acquire()
#         try:   
#             game.state = chase
#             mode_changed = False
#         finally:
#             lock.release()
#     print("chase")
    
#     if scatter_no < 4:
#         times.cancel()
#         times = Timer(20.0, scatter_on)
#         times.start()

#     else:
#         times.cancel()



if __name__ == "__main__":
    main()
