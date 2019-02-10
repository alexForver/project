# reference: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# USAGE: tracking a colored object and draw it's trajectory
# modify buffer to change the length of contrail 
# modify Lower and Upper to change the color filtering

from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument('-c','--camera',help = 'Use camera of laptop', action = 'store_false')
ap.add_argument('-w','--webcam',help = 'Use webcamera',action = 'store_false')
#buffer --length of previous positions
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size") 
args = vars(ap.parse_args())

Lower = (73, 107, 52)
Upper = (192, 255, 132)
pts = deque(maxlen=args["buffer"])

if not(args['camera']):
    vs = cv2.VideoCapture(0)

if not(args['webcam']):
    vs = cv2.VideoCapture(1)
    
time.sleep(2.0)

while True:
    frame = vs.read()
    frame = frame[1] 
    
    if frame is None:
        break
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        #((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center=(int(M["m10"] / M["m00"]),int(M["m01"]/M["m00"]))
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame,center, 5, (255, 255, 255), -1)
        #only proceed if the radius meets a minimum size
        #if radius > 10
        #cv2.circle(frame,(int(x),int(y),int(radius)),(0,255,255),2)
        #
        
    pts.appendleft(center)
    
    for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


vs.release()
cv2.destroyAllWindows()
