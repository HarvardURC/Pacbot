#logitech camera notes: (change using hardware options sections) 
#autofocus off
#autowhite balance off
#focus distance to infinty
# for finding upper and lower boundary :
# https://github.com/jrosebr1/imutils/blob/master/bin/range-detector

#this is a modified version of the ball-tracking software at
#http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

#use pts to access a dequeue containing the sticker center point.

# video usage:
# python robot_tracking.py --video [filename].mp4
# webcam usage:
# python robot_tracking.py 

# packages needed
from collections import deque
import numpy #must be installed
import argparse
import imutils #must be installed
import cv2 #must be installed

#setup argument parse
ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video",
    help = "video file path (optional), else webcam will be used")
d_argument("-b", "--buffer", type=int, default=2, help="max buffer size")

args = vars(ap.parse_args())
	
"""
Define lower and upper boundaries for coloured sticker
Initialize list of events
"""
stickerLower =
stickerUpper = #XKCD find using range-detecter script in imutils
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    #grab current frame
    (grabbed, frame) = camera.read()

    #if using video and no frame grabbed
    #then end of video reached
    if args.get("video") and not grabbed:
        break

    #resize the frame, blur and convert to HSV colour space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #construct a mask for the sticker colour, then perform
    #series of dilations and erosions to remove small blobs left
    mask = cv2.inRange(hsv, stickerLower, stickerUpper)
    mask = cv2.erode(mask, None iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #find contours of the sticker
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cvs2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    #may need something here for if there are no contours
    if len(cnts) < 0:
        print("contour error")
        break
        
    #proceed if a single contour found
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    #update points queue
    pts.appendLeft(center)

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
	break    

#camera cleanup and close open windows
camera.release()
cv2.destroyAllWindows()

	
	

