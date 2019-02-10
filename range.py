# reference: https://github.com/jrosebr1/imutils/blob/master/bin/range-detector
# 
# USAGE: to detect the HSV range of an object
# (pyhton) range.py --camera (turn on the camera of laptop)
#or
# (python) range.py --webcam (turn on the webcam)

import cv2
import argparse
import time

def nothing(x):
    pass


def setup_trackbars():
    cv2.namedWindow("Trackbars") 
    for i in ["MIN","MAX"]:
        for j in ["H","S","V"]:
            cv2.createTrackbar("%s_%s"%(j,i),"Trackbars",0,255,nothing)
    
def get_arguments():
    ap = argparse.ArgumentParser(description = 'choose the camera')
    ap.add_argument('-c','--camera',help = 'Use camera of laptop', action = 'store_false')
    ap.add_argument('-w','--webcam',help = 'Use webcamera',action = 'store_false')
    args = vars(ap.parse_args())
    
    return args


def get_trackbar_values():
    values = []
    
    for i in ["MIN","MAX"]:
        for j in ["H","S","V"]:
            v = cv2.getTrackbarPos("%s_%s"%(j,i),"Trackbars")
            values.append(v)
    
    return values

def main():
    args = get_arguments()
    
    if not(args['camera']):
        cap = cv2.VideoCapture(2)

    if not(args['webcam']):
        cap = cv2.VideoCapture(0)
    
    time.sleep(2.0)
        
    setup_trackbars()
    
    while True:
        ret, frame = cap.read()
         
        if not ret:
            break
        
        frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values()
        
        thresh = cv2.inRange(frame_to_thresh,(v1_min,v2_min,v3_min),(v1_max,v2_max,v3_max))
        
        cv2.imshow('frame', frame)
        cv2.imshow('thresh', thresh)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
        
if __name__ == '__main__':
    main()
