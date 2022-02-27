#!/bin/bash

ttab "echo -n -e \"\033]0;My Window Name\007\" && ./server.py"
ttab "echo -n -e \"\033]0;My Window Name\007\" && ./gameEngine.py"
ttab "echo -n -e \"\033]0;My Window Name\007\" && ./visualize.py -p -s -w"
./keyboardInput.py

osascript -e 'tell application "Terminal" to close (every window whose name contains "My Window Name")' &