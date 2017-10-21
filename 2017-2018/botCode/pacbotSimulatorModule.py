#!/usr/bin/env python3

import os
import robomodules as rm
import variables as var
from messages import MsgType, message_buffers, PacmanState

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = .5


class PacbotSimulatorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.current_location = var.pacbot_starting_pos
        self.current_command = None


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PacmanCommand:
            self.current_command = msg.dir

    def tick(self):
        curr_x = self.current_location[0]
        curr_y = self.current_location[1]
        # Update Pacman's location based on the command
        if self.current_command == PacmanCommand.Direction.NORTH:
            self.current_location = (curr_x, curr_y + 1)
        elif self.current_command == PacmanCommand.Direction.SOUTH:
            self.current_location = (curr_x, curr_y - 1)
        elif self.current_command == PacmanCommand.Direction.EAST:
            self.current_location = (curr_x + 1, curr_y)
        elif self.current_command == PacmanCommand.Direction.WEST:
            self.current_location = (curr_x - 1, curr_y)

        # Create a new PacmanState message and broadcast the new location
        new_msg = PacmanState.AgentState()
        new_msg.x = self.current_location[0]
        new_msg.y = self.current_location[1]
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)


def main():
    module = PacbotSimulatorModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
