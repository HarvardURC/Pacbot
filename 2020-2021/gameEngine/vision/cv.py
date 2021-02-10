import numpy as np
import cv2
import robomodules as rm
from pacbot.grid import grid
from messages import *
from .helpers import *
from .grid import grid
from .variables import *

FREQUENCY = 30

class MovementProcessor(rm.ProtoModule):
    def __init__(self, addr, port, cam_id, y_off, height, width, show_windows):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(3,640)
        self.cap.set(4,360)
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
        if np.array_equal(warped, []):
            return

        warped = warped[:,20:-20]

        warped_blur = cv2.medianBlur(warped, 5)
        hsv = cv2.cvtColor(warped_blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        res = cv2.bitwise_and(warped, warped, mask=mask)
        res = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
        imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(imgray,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        

        sector_h = imgray.shape[0]/self.height
        sector_w = imgray.shape[1]/self.width

        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            if cv2.contourArea(c) > 100:
                skip = False
                x, y, w, h = cv2.boundingRect(c)
                x_c = x + 0.5*sector_w
                y_c = (imgray.shape[0] - y) - 1.5*sector_h
                b_y = int(self.y_off + round(y_c/sector_h))
                b_x = int(round(x_c/sector_w))
                if b_y >= self.y_off + self.height - 1 and self.y_off > 1:
                    b_y = self.y_off + self.height - 2
                elif b_y < 1:
                    b_y = 1
                if b_x < 1:
                    b_x = 1
                elif b_x > self.width:
                    b_x = self.width
                if grid[b_x][b_y] == I:
                    skip = True
                print((b_x, b_y))
                if not skip:
                    buf = PacmanState.AgentState()
                    buf.x = b_x
                    buf.y = b_y
                    self.client.write(buf.SerializeToString(), MsgType.PACMAN_LOCATION)

        if self.show_windows:
            cv2.imshow('warp',warped) #Warped Image based on the corners detected.

    def kill(self):
        cv2.destroyAllWindows()
        self.cap.release()
