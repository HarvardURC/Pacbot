# Pacbot 2021-22 gameEngine

## Requirements
To run the gameEngine, the dependencies listed in the ***src/environment.yml*** need to be installed. The ***src/environment.yml*** file is an exported Conda environment, so creating a Conda environment from this is recommended.

## Running the gameEngine

To run the gameEngine, first run the server and then run each of the module proccesses separately. 

Specifically, run the following files:

1. `./server.py`
This creates a server for communicating between the different modules.

2. `./gameEngine.py`
This runs the game. Type r to restart, p to unpause/pause, and q to quit.

3. `./visualize.py` OR `./terminalPrinter.py`

*visualize.py* displays the game graphics - see **Visualizer** for info regarding its command line arguments.

*terminalPrinter.py* will instead display the game in the terminal.

4. `./keyboardInput.py` OR `./cameraReader.py`

*keyboardInput.py* allows you to provide w,a,s,d commands for moving the PacBot (you must be in this terminal window to provide these commands).

*cameraReader.py* will instead use the connected cameras to track where the PacBot is on the game board and relay that information to the gameEngine.

## Visualizer

The visualizer takes 2 command line arguments:
- `-w` - If this is supplied, then the visualizer will draw the maze walls.
- `-p` - If this is supplied, then the visualizer will draw pacman.

## KeyboardInput

When running the keyboard input, you can move pacman using the w,a,s,d keys.
