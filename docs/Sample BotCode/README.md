# Sample BotCode


## Files/Folders

### samplePacbotModule.py

This custom module is a subclass of the ProtoModule class from RoboModules. The module is initialized with a connection to the game engine server. When an instance of the module is running (by calling the run method), the method msg_received is called whenever the module receives a message from the game engine server. If the msg_type is MsgType.LIGHT_STATE, this message is the game state. This state contains the game state information (as outlined in the rules for the game). If desired, the tick function is helpful for running custom code at a desired frequency (in Hz). More details on how to use Robomodules in your own project if desired can be found in the Robomodules documentation (https://github.com/HarvardURC/robomodules).

### messages

This folder contains the Protobuf definitions of the messages your bot will be receiving. There is no need to edit this code.

### robomodules

Robomodules is a custom Python framework maintained by the Harvard Undergraduate Robotics Club that allows independent modular components to communicate via TCP traffic. The 'samplePacbotModule.py' is one module that communicates with the game engine, another module. No need to edit this code.

## Running the Sample Code

1. Run the game engine. See 'src/gameEngine' for information. Essentially, one must run 'src/gameEngine/server.py' and 'src/gameEngine/gameEngine.py'.

2. Run 'samplePacbotModule.py'. The state of the game should be printed on the screen.