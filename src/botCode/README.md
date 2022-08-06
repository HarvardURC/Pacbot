# PacBot 2021-22 Bot Code

This directory contains all of the code for the Harvard team's PacBot. Participating teams can refer to this code when designing their own bots if they'd like.

## How it works

The botcode will connect to the gameEngine Server in order to receive messages, but it will also run its own separate robomodules server for internal use. `server.py` is the internal server, `pacbotCommsModule.py` is a module that connects to both the gameEngine server and the local server, listens to the gameEngine's LightState messages and forwards them to the local server. 

## High Level Strategy Code

The high level strategy for the robot is in 'heuristicHighLevelModule.py'. This receives the game state from the local server regarding the robot's location and the location of the ghosts. It makes a decision regarding where to move the bot. It sends a PACMAN_COMMAND message to tell the bot which direction to go.

Run './heuristicHighLevelModule.py' to run the high level module.


## Low Level Code

The module 'directionLowLevelModule.py' is our current low level code module. It receives direction commands from the high level module and makes decisions on how to move the motors.

Motor movement is managed through PID loops dependent on the IR sensors. See 'low_level' directory for related code.


## Requirements

- See the 'src/environment.yml' for a conda environment with the necessary Python3 requirements.
- In order to run the bot code, you need to already have a gameEngine server running.

## How to run the code

1. Start the game engine - follow instructions in src/gameEngine.
2. Start the local bot server. 
  - Supply the correct server address:port combination in `server.py` either through environment variables or by changing the default values in the code itself. Like the game engine server, the bot server should bind to your computer's local IP address.
  - run `./server.py`.
3. Start the communications module by running `./pacbotCommsModule.py`.
  - Make sure the SERVER_ADDRESS:SERVER_PORT is the address of the game engine server and that you are on the same WiFi network as the game engine server. Make sure the LOCAL_ADDRESS:LOCAL_PORT is the adress of the local bot server (and that you're on the same WiFi network as the local server).
4. Start all other desired modules (i.e. heuristicHighLevelModule and directionLowLevelModule).


## Other Modules

pacbotSimulatorModule.py

Running this module will allow you to simulate the heuristicHighLevelModule playing the game. It communicates the moves the high level module makes to the game engine.

keyboardModule.py

This module should allow you to control the PacBot with your keyboard AWSD keys.
