#!/usr/bin/env python3

import os
import robomodules as rm
from messages import MsgType, message_buffers, PacmanState

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

class pacbotSimulatorModule(rm.protoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND]
        super().__init__(addr, port, message_buffers, MsgType, self.subscriptions)  # Frequency is 0 by default
        self.current_location = (14, 7)  # I can't figure out how to import the starting location of pacbot


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PacmanCommand:
            curr_x = self.current_location[1]
            curr_y = self.current_location[2]

            # Update Pacman's location based on the command
            if msg.Direction == 1:
                self.current_location = (curr_x, curr_y + 1)
            elif msg.Direction == 2:
                self.current_location = (curr_x, curr_y - 1)
            elif msg.Direction == 3:
                self.current_location = (curr_x + 1, curr_y)
            elif msg.Direction == 4:
                self.current_location = (curr_x - 1, curr_y)

            # Create a new PacmanState message and broadcast the new location
            new_msg = PacmanState.AgentState()
            new_msg.x = self.current_location[1]
            new_msg.y = self.current_location[2]
            self.write(new_msg, MsgType.PACMAN_LOCATION)


    def tick(self):
        return
