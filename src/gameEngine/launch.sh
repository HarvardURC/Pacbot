#!/bin/bash


gnome-terminal --tab --command="./server.py" --tab --command="./gameEngine.py" --tab --command="./visualize.py -w -p -s";

if ($1 != " "); then
    (cd ../botCode/; ./launch.sh) 
else
    ./keyboardInput.py;
fi