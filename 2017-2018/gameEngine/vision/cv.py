import numpy as np
import cv2
import robomodules as rm
from pacbot.grid import grid
from messages import *

FREQUENCY = 0

class MovementProcessor(rm.ProtoModule):
    def __init__(self, addr, port):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
	# initialization stuff here
        
    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return


    def tick(self):
	# stuff in while loop here
	bot_loc = (0, 0) # TODO change this
	
        buf = PacmanState.AgentState()
        buf.x = bot_loc[0]
        buf.y = bot_loc[1]
        self.client.write(buf.SerializeToString(), MsgType.PACMAN_LOCATION)
