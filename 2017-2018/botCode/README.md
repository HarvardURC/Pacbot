# PacBot 2017-18 Bot Code

## How it works

The botcode will connect to the gameEngine Server in order to receive messages, but it will also run it's own separate robomodules server for internal use. `server.py` is the internal server, `pacbotCommsModule.py` is a module that connects to both the gameEngine server and the local server, listens to the gameEngine's LightState messages and forwards them to the local server. `samplePacbotModule.py` gets the game state from the local server and prints it out. When developing new local modules, base them off of `samplePacbotModule.py`.

## Requirements

- The botcode requires `python3`.
- In order to run the bot code, you need to already have a gameEngine server running.

## How to run the code

1. Start the server.
  - Supply the correct server address:port combination the `server.py` either through environment variables or by changing the default values in the code itself.
  - run `./server.py`.
2. Start the communications module by running `./pacbotCommsModule.py`.
3. Start all other modules.
