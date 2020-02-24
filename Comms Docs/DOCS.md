# Game Engine Communication Information

For communication, PacBot uses Robomodules, a custom python framework for handling
communication between modular components using TCP traffic. The game uses a
single Robomodule server; teams' bots will connect to this server to receive
information about the Pacman game state. Specific documentation for Robomodules
can be found here: https://github.com/HarvardURC/robomodules

To connect to the running game engine, teams must run their own
Robomodule ProtoModule. A sample module is in this folder. The custom
module is a subclass of the ProtoModule class. The module is initialized with
a connection to the game engine server. When an instance of
the module is running (by calling the run method), the method msg_received is
called whenever the module receives a message from the game engine server. If
the msg_type is MsgType.LIGHT_STATE, this message is the game state. This state
contains the game state information (as outlined in the rules for the game). If
desired, the tick function is helpful for running custom code at a desired
frequency (in Hz). More details on how to use Robomodules in your own project if
desired can be found in the Robomodules documentation.
