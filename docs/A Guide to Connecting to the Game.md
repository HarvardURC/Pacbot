# How to run the game and connect to your bot - A Guide

This guide outlines the step by step process for running the PacMan game and connecting your robot to the game.

1. Ensure you have the necessary Python libraries installed as outlined in 'src/requirements.txt'. We recommend using a Conda environment; an image of our environment is provided in 'src/evironment.yml'.

2. Ensure your robot and computer (that's running the PacMan game) are on the same WiFi network.

3. Set the bind address for the PacMan game server.

The computer running the game will have a server that forwards messages about the game state to your robot. The bind address for this server should be the local IP address of your game computer.

Set the bind address via ```export BIND_ADDRESS=myIpAddress``` where ```myIpAddress``` is the local IP address of your game computer. Run this command in your shell on the game computer and on your robot.

4. Run the game on your computer.

Follow the instructions on 'src/gameEngine'. You should specifically run 'src/gameEngine/server.py', 'src/gameEngine/gameEngine.py', and 'src/gameEngine/visualize.py'.

5. Run the sample botcode on your robot.

Run 'docs/Sample BotCode/samplePacbotModule.py' on your robot. The state of the game should be printed.
