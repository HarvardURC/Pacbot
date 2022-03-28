# Pacbot 2021-22 gameEngine

## Requirements
To run the gameEngine, the dependencies listed in the ***src/environment.yml*** need to be installed. The ***src/environment.yml*** file is an exported Conda environment, so creating a Conda environment from this is recommended.

Currently, the game engine only runs on **Mac** and **Linux** computers (not Windows). We are working on fixing issues with the Python graphics package to allow the game engine to run on Windows computers.

## Running the gameEngine

To run the gameEngine, first run the server and then run each of the module proccesses separately. 

Specifically, run the following files:

1. `./server.py`
This creates a server for communicating between the different modules. The modules that run the game connect to this server. In addition, the PacBot will connect to this server to receive the game state. The server automatically binds to 'localhost' for testing purposes, but should be bound to the computer's local IP address when attempting to communicate with the robot over WiFi. Set the environment variable BIND_ADDRESS to control the IP address of the server. In addition, a different port may be needed than the default; set the environment variable BIND_PORT to control this as well.

2. `./gameEngine.py`
This runs the game. Type r to restart, p to unpause/pause, and q to quit.

3. `./visualize.py` OR `./terminalPrinter.py`

*visualize.py* displays the game graphics - see **Visualizer** for info regarding its command line arguments.

*terminalPrinter.py* will instead display the game in the terminal.

4. `./keyboardInput.py` OR `./cameraReader.py`

*keyboardInput.py* allows you to provide w,a,s,d commands for moving the PacBot (you must be in this terminal window to provide these commands).

*cameraReader.py* will instead use the connected cameras to track where the PacBot is on the game board and relay that information to the gameEngine.

## Visualizer

The visualizer takes 3 command line arguments:
- `-w` - If this is supplied, then the visualizer will draw the maze walls.
- `-p` - If this is supplied, then the visualizer will draw pacman.
- `-s` - If this is supplied, then the visualizer should fit the entire game onto your computer screen. 
         If not, then you can supply a specific square size by inputting `-s=x`, where x is some integer.
         Default square size without `-s` is 31, square size with `-s` is 25.

## KeyboardInput

When running the keyboard input, you can move pacman using the w,a,s,d keys.
