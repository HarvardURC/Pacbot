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
import signal
from threading import Thread, Lock
import time


restart = False


lock = Lock()

from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()



lay = layout.getLayout("pacbotLayout.lay")
pacbot = PacBot((23,13), "right")
game = GameState(copy.deepcopy(grid), lay, pacbot)
botTracker = BotTracker()
graphics = None
session = True

app = Flask("Pacman")

@app.route('/pac-bot')
def pacBot():
    # if game.game_on:
    #     response = {}
    #     # response['pacbot'] = {
    #     #     'x': game.pacbot.pos['current'][0],
    #     #     'y': game.pacbot.pos['current'][1]
    #     # }
    #     response['ghost1'] = {
    #         'x': game.red.pos['current'][0],
    #         'y': game.red.pos['current'][1]
    #     }
    #     response['ghost2'] = {
    #         'x': game.pink.pos['current'][0],
    #         'y': game.pink.pos['current'][1]
    #     }
    #     response['ghost3'] = {
    #         'x': game.orange.pos['current'][0],
    #         'y': game.orange.pos['current'][1]
    #     }
    #     response['ghost4'] = {
    #         'x': game.blue.pos['current'][0],
    #         'y': game.blue.pos['current'][1]
    #     }
    #     if (game.state == frightened):
    #         response['specialTimer'] = game.frightened_counter
    #     return jsonify(response)
    # else:
    #     return jsonify({'stop': True})
    return jsonify(getFormattedGameData())

def getFormattedGameData():
    if game.game_on:
        response = {}
        # response['pacbot'] = {
        #     'x': game.pacbot.pos['current'][0],
        #     'y': game.pacbot.pos['current'][1]
        # }
        response['ghost1'] = {
            'x': game.red.pos['current'][0],
            'y': game.red.pos['current'][1]
        }
        response['ghost2'] = {
            'x': game.pink.pos['current'][0],
            'y': game.pink.pos['current'][1]
        }
        response['ghost3'] = {
            'x': game.orange.pos['current'][0],
            'y': game.orange.pos['current'][1]
        }
        response['ghost4'] = {
            'x': game.blue.pos['current'][0],
            'y': game.blue.pos['current'][1]
        }
        if (game.state == frightened):
            response['specialTimer'] = game.frightened_counter
        return response
    else:
        return {'stop': True}

def xBee():
    xbee = Serial('/dev/cu.usbserial-DA00VDM1', 9600)
    m = dumps(getFormattedGameData())
    while True:
        try:
            xbee.write(m)
            time.sleep(.1)
        except KeyboardInterrupt:
            break
    xbee.halt
    xbee.close()

# def callback():
#     callbacks = q.get(False) #doesn't block
#     if callbacks == "hi":
#         lay = layout.getLayout("pacbotLayout.lay")
#         pacbot = PacBot((23,13), "right")
#         game = GameState(copy.deepcopy(grid), lay, pacbot)

#         graphics = PacmanGraphics(0.5)

#         graphics.initialize(game.gstate)
#         print("hi")
    

def main():
    global lay, pacbot, game, botTracker, graphics
    graphics = PacmanGraphics(0.95)

    graphics.initialize(game.gstate)
    graphics.update(game.gstate)

    
    position = botTracker.get_bot_location()
    direction = botTracker.get_bot_direction()
    pacbot.update(position, direction)
    
    # sched.add_job(callback, 'interval', seconds = 5)
    Thread(target = handleInput).start()
    Thread(target = appRunner).start()
    # Thread(target = xBee).start()
    Thread(target = gameUpdate(graphics)).start()
    Thread(target = trackerUpdate).start()
    

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
                    # if game.grid[position[0]][position[1]] != I and game.grid[position[0]][position[1]] != n:
                    #     print("true")
                    # else:
                    #     print("false")
                    # print(str(game.pacbot.pos[0]) + " " + str(game.pacbot.pos[1]))
                finally:
                    lock.release()
                time.sleep(.1)
            except KeyboardInterrupt:
                break
                


def gameUpdate(graphics):
    global game , play, pacbot, lay  , restart  
    # display start postions
    # display_game(game.pacbot,game.red,game.pink,game.orange,game.blue,game.score,game.lives,game.state,game.grid)
    

    if game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] == o:
        game.grid[game.pacbot.pos[0]][game.pacbot.pos[1]] = e
        game.score += 1
    
    counter = 1
    while session:
        if game.play:
            
         
            # time.sleep(.1)
        
            # if counter < 2:
            #     graphics.update(game.gstate)
            #     counter += 1
            # else:
            #     counter = 1
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
            lay = layout.getLayout("pacbotLayout.lay")
            pacbot = PacBot((23,13), "right")
            game = GameState(copy.deepcopy(grid), lay, pacbot)

            graphics = PacmanGraphics(0.5)
            graphics.initialize(game.gstate)
            graphics.update(game.gstate)



        
        # print(str(pacbot.pos[0]) + ' ' + str(pacbot.pos[1]))


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

# def restart():
#     global lay, game, graphics, pacbot

    
#     pacbot = PacBot((23,13), "right")
#     game = GameState(copy.deepcopy(grid), lay, pacbot)

#     graphics = PacmanGraphics(q, 0.5)

#     graphics.initialize(game.gstate)
#     print("hi")

    


if __name__ == "__main__":
    main()




