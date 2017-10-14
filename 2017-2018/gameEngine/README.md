# Pacbot 2017-18 gameEngine

## Requirements
To run the gameEngine you need the following:
- Python 3
- Pygame (for the visualizer)
- OpenCV (for the computer vision module)

In order to add new message types you need the Google Protocol Buffer compiler for python.

## Running the gameEngine

To run the gameEngine, first run the server and then run each of the module proccesses separately.
`./server.py`
`./gameEngine.py`
`./visualizer.py` OR `./terminalPrinter.py`
`./keyboardInput.py` OR `./gameraReader.py`

## Visualizer

The visualizer takes 2 command line arguments:
- `-w` - If this is supplied, then the visualizer will draw the maze walls.
- `-p` - If this is supplied, then the visualizer will draw pacman.

## KeyboarInput

When running the keyboard input, you can move pacman using the w,a,s,d keys.
