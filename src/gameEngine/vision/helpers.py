import cv2
from .transform import *
import numpy as np
from .variables import lower_green, upper_green

def valid(contours):
    x,y = [],[]
    for i in contours:
        x.append(i[0][0][0])
        y.append(i[0][0][1])
    
    for i in range(3):
        for j in range(i+1, 4):
            if abs(x[i]-x[j]) < 100:
                return 0
            if abs(y[i]-y[j]) < 10:
                return 0
    return 1

def get_bounds_distance(a, b):
    if a[0] > b[0]:
        x_h = a[0]
        x_l = b[0]
        w_l = b[2]
    else:
        x_h = b[0]
        x_l = a[0]
        w_l = a[2]

    if a[1] > b[1]:
        y_h = a[1]
        y_l = b[1]
        h_l = b[3]
    else:
        y_h = b[1]
        y_l = a[1]
        h_l = a[3]
    dist = 0
    y_diff = y_h - y_l - h_l 
    if y_diff > 0:
        dist += y_diff
    
    x_diff = x_h - x_l - w_l
    if x_diff > 0:
        dist += x_diff
    return dist

def get_center_distance(a, b):
    center_a = (a[0] + a[2]/2, a[1] + a[3]/2)
    center_b = (b[0] + b[2]/2, b[1] + b[3]/2)
    return ((abs(center_a[0] - center_b[0]))**2 + (abs(center_a[1] - center_b[1]))**2)**0.5

def merge_bounds(a, b):
    x = a[0] if a[0] < b[0] else b[0]
    y = a[1] if a[1] < b[1]  else b[1]
    x_end = a[0] + a[2] if a[0] + a[2] > b[0] + b[2] else b[0] + b[2]
    y_end = a[1] + a[3] if a[1] + a[3] > b[1] + b[3] else b[1] + b[3]

    w = x_end - x
    h = y_end - y

    return (x, y, w, h)

def warp_image(frame):

    # Prepare the image for finding dots
    frame = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    res = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    
    # Find contours
    contours, _ = cv2.findContours(imgray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # At this point we will filter our contours.
    # We will merge contours that are nearby together
    # and discard contours that are too small
    rects = []
    for c in contours:
        rect = cv2.boundingRect(c)
        if rect[2]*rect[3] > 30:
            rects.append(rect)
    if len(rects) < 4:
        return []
    merged_rects = []
    candidates = rects
    
    # Go through all rectangles and get their distance to other rectangles.
    # If they are close enough, then merge them.
    while len(candidates) > 0:
        next_candidates = []
        r1 = candidates[0]
        for r2 in candidates[1:]:
            dist = get_bounds_distance(r1, r2)
            if dist < 10:
                r1 = merge_bounds(r1, r2)
            else:
                next_candidates.append(r2)
        merged_rects.append(r1)
        candidates = next_candidates

    # Sort the merged rectangles by area
    areas = np.array([w*h for x, y, w, h in merged_rects])
    idxs = areas.argsort()
    rects_sorted = np.array([merged_rects[i] for i in idxs])

    # If ther are at least 4 rectangles, then perform the warp
    if len(rects_sorted) >= 4:

        # Add the centers of the rectangles to a new warp input
        warp_points = np.vstack([(float(i[0] + i[2]/2), float(i[1] + i[3]/2)) for i in rects_sorted[:4]])
        
        warp = np.array(warp_points, dtype = "float32")
        return four_point_transform(frame, warp)
    else:
        return []

