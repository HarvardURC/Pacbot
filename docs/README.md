# PacBot Documentation

See 'A Guide to Connecting to the Game' for the step by step process to connect your robot to the PacMan game.

## Arena

'Arena Documentation' contains images of the life sized PacMan game board along with a SLDPRT file containg the CAD design of the arena. Overall, the arena mimics the PacMan game where each path is 7 inches wide. Bots should be smaller than 7 inches by 7 inches to effectively navigate the arena. The arena is currently made of wooden material, and the walls of the channels are painted white.

The arena is programmatically divided into a 28 x 31 grid. The ghost and PacBot locations are read out with respect to this grid. For details on the structure of this grid, 'src/gameEngine/pacbot/grid.py'.

## Sample Bot Code

The PacBot game uses WiFi to send the game state to participating robots; thus all participating teams must have WiFi compatible robots. To do this, PacBot uses Robomodules, a custom Python3 framework for handling communication between modular components using TCP traffic. The game uses a single Robomodules server; teams' bots will connect to this server to receive information about the Pacman game state. Specific documentation for Robomodules can be found here: https://github.com/HarvardURC/robomodules

To connect to the running game engine, teams must run their own Robomodules ProtoModule. The 'Sample BotCode' in this folder contains an example ProtoModule. Please see the 'Sample BotCode' for information regarding the ProtoModule and how it receives the game state.

## Public Designs

The 'Public Designs' folder contains information regarding the EE/ME design of last year's PacBot for the Harvard Undergraduate Robotics Club.