# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 00:31:28 2019

@author: qwq
"""

import cv2
import time

count = 0
vs = cv2.VideoCapture(0)

time.sleep(2.0)

while True:
    ret, frame = vs.read()
    #frame = frame[1]
    #frame = cv2.QueryFrame(vs)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite("C:/Users/qwq/Desktop/image{}.jpg".format(count),frame)
        count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vs.release()
cv2.destroyAllWindows()
