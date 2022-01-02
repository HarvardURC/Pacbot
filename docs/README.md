# PacBot Documentation

## Arena

'Arena Documentation' contains images of the life sized PacMan game board along with a SLDPRT file containg the CAD design of the arena. Overall, the arena mimics the PacMan game where each path is 7 inches wide. Bots should be smaller than 7 inches by 7 inches to effectively navigate the arena. The arena is currently made of wooden material, and the walls of the channels are painted white.

## Sample Bot Code and Communication

The PacBot game uses WiFi to send the game state to participating robots; thus all participating teams must have WiFi compatible robots. To do this, PacBot uses Robomodules, a custom Python3 framework for handling communication between modular components using TCP traffic. The game uses a single Robomodules server; teams' bots will connect to this server to receive information about the Pacman game state. Specific documentation for Robomodules can be found here: https://github.com/HarvardURC/robomodules

To connect to the running game engine, teams must run their own Robomodules ProtoModule. The 'Sample BotCode' in this folder contains an example ProtoModule. Please see the 'SampleBotCode' for information regarding the ProtoModule and how it receives the game state.

## Public Designs

The 'Public Designs' folder contains information regarding the EE/ME design of last year's PacBot for the Harvard Undergraduate Robotics Club.