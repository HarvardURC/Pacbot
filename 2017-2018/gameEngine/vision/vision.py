import cv2, transform
import numpy as np
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

cap = cv2.VideoCapture(0)
warp = [(0,0) for i in range(4)]
warp_on = 0

height = int(26) #(Camera sees the vertical Axis)
width = int(14) #(Camera sees the horizontal axis)

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


while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #For Black Dots
    lower_red = np.array([20,30,180])
    upper_red = np.array([65,60,250])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    im2 = cv2.medianBlur(im2, 5)

#   kernel = np.ones((5,5),np.float32)/25
#   im2 = cv2.filter2D(im2,-1,kernel)

    cv2.drawContours(frame, contours, -1, (100,255,255), 10)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contours) != 0: #and not warp_on:
	print len(contours)
        cv2.drawContours(im2, contours, -1, 255, 3)
	
	warp_on = 1
		
	warp = [(float(i[0][0][0]), float(i[0][0][1])) for i in contours]

	warp = vstack(warp)
	#print warp
	centroids,_ = kmeans(warp,4)
	idx,_ = vq(warp,centroids)

	#print centroids
	warp = [(i[0],i[1]) for i in centroids]
	#print warp
	#Fix the STRING ISSUE ##############
	warp = np.array(eval(str(warp)), dtype = "float32")	
	print "Got xD"
        #print contours.sort(key = cv2.contourArea)
        #print len(contours)
        #print cv2.contourArea(c)
        #        print len(contours)

    else:
	pass
	#if not warp_on:
        	#print("No Contours xD")

    if warp_on:
	 warped = transform.four_point_transform(frame, warp)

         hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
         lower_red = np.array([20,100,100])
         upper_red = np.array([30,255,255])
         mask = cv2.inRange(hsv, lower_red, upper_red)
         res = cv2.bitwise_and(warped, warped, mask=mask)
         imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	 ret,thresh = cv2.threshold(imgray,127,255,0)
         im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
         im2 = cv2.medianBlur(im2,15)

         cv2.drawContours(im2, contours, -1, (100,255,200), 3)

         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	 
	 sector_h = np.size(im2, 1)/height
	 sector_w = np.size(im2, 0)/width
	 #print sector_h, sector_w 

         if len(contours) != 0:
             cv2.drawContours(res, contours, -1, 255, 3)

             c = max(contours, key = cv2.contourArea)
             if cv2.contourArea(c) > 10000:
                 print c[0][0][0]/sector_h, c[0][0][1]/sector_w
		
	     #print c[0][0][0],c[0][0][1]	
	     #return (x,y)
	     # C[0] is ; C[1] is Y.

	 cv2.imshow('warp',warped) #Warped Image based on the corners detected.
	 cv2.imshow('im',im2) #Image that localises the corners and applies the filters to it.

    cv2.imshow('frame',frame) #Original Frame
#   cv2.imshow('mask',mask)
#   cv2.imshow('res',res)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
