#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
from variables import lower_green, upper_green, lower_yellow, upper_yellow

CAM_NUM = 1
green = True

def nothing(x):
    pass

class ViewImages:
    """
    Use the RGB camera to find the largest blue object
    """

    def __init__(self):

        # Set thresholds for color detection and thresholding
        if green:
            self.thresh_low = lower_green
            self.thresh_high = upper_green 
        else:
            self.thresh_low = lower_yellow
            self.thresh_high = upper_yellow 

    def run(self):
       # Create a black image, a window
        img_width = 512
        img = np.zeros((300, img_width, 3), np.uint8)
        cv2.namedWindow('thresholds')

        # Create trackbars for color change
        cv2.createTrackbar('H (low)', 'thresholds', 0, 255, nothing)
        cv2.createTrackbar('S (low)', 'thresholds', 0, 255, nothing)
        cv2.createTrackbar('V (low)', 'thresholds', 0, 255, nothing)
        cv2.createTrackbar('H (high)', 'thresholds', 0, 255, nothing)
        cv2.createTrackbar('S (high)', 'thresholds', 0, 255, nothing)
        cv2.createTrackbar('V (high)', 'thresholds', 0, 255, nothing)
        
        # Set with saved/inial values
        cv2.setTrackbarPos('H (low)', 'thresholds', self.thresh_low[0])
        cv2.setTrackbarPos('S (low)', 'thresholds', self.thresh_low[1])
        cv2.setTrackbarPos('V (low)', 'thresholds', self.thresh_low[2])
        cv2.setTrackbarPos('H (high)', 'thresholds', self.thresh_high[0])
        cv2.setTrackbarPos('S (high)', 'thresholds', self.thresh_high[1])
        cv2.setTrackbarPos('V (high)', 'thresholds', self.thresh_high[2])
        camera = cv2.VideoCapture(CAM_NUM)
        camera.set(3, 960)
        camera.set(4, 540)
        while True:
            cv2.imshow('thresholds', img)

            # Get current positions of trackbars
            h = cv2.getTrackbarPos('H (low)', 'thresholds')
            s = cv2.getTrackbarPos('S (low)', 'thresholds')
            v = cv2.getTrackbarPos('V (low)', 'thresholds')
            img[:, :int(img_width/2)] = [h, s, v]
            self.thresh_low = np.array([h, s, v])
            
            h = cv2.getTrackbarPos('H (high)', 'thresholds')
            s = cv2.getTrackbarPos('S (high)', 'thresholds')
            v = cv2.getTrackbarPos('V (high)', 'thresholds')
            img[:, int(img_width/2):] = [h, s, v]
            self.thresh_high = np.array([h, s, v])
            
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            

            return_value, cv_image = camera.read()
            cv_image = self.threshold(cv_image)
            # Display the modified image
            cv2.imshow('picture', cv_image)
            cv2.waitKey(3)
            sleep(0.03)

    def threshold(self, img):
        """
        Apply the threshold to the image to get only blue parts
        :param img: RGB camera image
        :return: Masked image
        """

        # Apply a blur
        img = cv2.medianBlur(img, 5)
        # Convert image to easier-to-work-with HSV format
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Threshold to get only blue values
        mask = cv2.inRange(img_hsv, self.thresh_low, self.thresh_high)
        masked_img = cv2.bitwise_and(img, img, mask=mask)

        return masked_img

if __name__ == '__main__':
    viewer = ViewImages()
    viewer.run()
