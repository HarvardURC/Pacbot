# Pacbot 2017-18 gameEngine

## Requirements
To run the gameEngine you need the following:
- Python 3
- Pygame (for the visualizer)
- OpenCV (for the computer vision module)
- Protobuf (for the server)


In order to add new message types you need the Google Protocol Buffer compiler for python.

## Running the gameEngine

To run the gameEngine, first run the server and then run each of the module proccesses separately.
1. `./server.py`

2. `./gameEngine.py`

3. `./visualize.py` OR `./terminalPrinter.py`

4. `./keyboardInput.py` OR `./cameraReader.py`

## Visualizer

The visualizer takes 3 command line arguments:
- `-w` - If this is supplied, then the visualizer will draw the maze walls.
- `-p` - If this is supplied, then the visualizer will draw pacman.
- `-s` - If this is supplied, then the visualizer should fit the entire game onto your computer screen. 
         If not, then you can supply a specific square size by inputting `-s=x`, where x is some integer.
         Default square size without `-s` is 31, square size with `-s` is 25.

## KeyboardInput

When running the keyboard input, you can move pacman using the w,a,s,d keys.
