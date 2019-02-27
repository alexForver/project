# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 12:37:38 2019

@author: qwq
"""
import cv2
import numpy
import time

dist = numpy.loadtxt('C:/Users/qwq/Desktop/image/cameraDistortion.txt', delimiter = ',')
mtx = numpy.loadtxt('C:/Users/qwq/Desktop/image/cameraMatrix.txt',delimiter = ',')

vs = cv2.VideoCapture(0)

time.sleep(2.0)

while True:
    ret, frame = vs.read()
    #frame = frame[1]
    h, w = frame.shape[:2]
    
    #newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    #mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,mtx,(w,h),5)
    
    #crop the image
    #x,y,w,h = roi
    #dst = dst[y:y+h, x:x+w]
    
    frame = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
    
    cv2.imshow("Frame",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vs.release()
cv2.destroyAllWindows()
