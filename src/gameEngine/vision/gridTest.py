import numpy as np
import cv2
import robomodules as rm
from pacbot.grid import grid
from messages import *
from .helpers import *
from .grid import grid
from .variables import *

FREQUENCY = 60

class MovementProcessor(rm.ProtoModule):
    def __init__(self, addr, port, cam_id, y_off, height, width, show_windows):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(3,960)
        self.cap.set(4,540)
        self.y_off = y_off
        self.height = height
        self.width = width
        self.show_windows = show_windows
        
    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return


    def tick(self):
        # stuff in while loop here
        _, frame = self.cap.read()

        if self.show_windows:

            cv2.imshow('frame',frame) #Original Frame

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                return

        warped = warp_image(frame)
        warped = warped[:,20:-20]
        imgray = warped
        if np.array_equal(warped, []):
            return

        sector_h = imgray.shape[0]/self.height
        sector_w = imgray.shape[1]/self.width

        for x in range(self.width):
            x_c = (x+1)*sector_w
            delta_x = 2.5*(x_c/imgray.shape[1] - 0.5)
            delta_x = 0
            x_c += delta_x*sector_w
            for y in range(self.height):
                y_c = (self.height - (y+1)) * sector_h
                delta_y = 1*(y_c/imgray.shape[0] - 0.5)
                delta_y = 0
                y_c += delta_y*sector_h
                cv2.circle(warped, (int(x_c), int(y_c)), 4, color=(0, 0, 255), thickness=-1)

        
        if self.show_windows:
            cv2.imshow('warp',warped) #Warped Image based on the corners detected.

    def kill(self):
        cv2.destroyAllWindows()
        self.cap.release()
