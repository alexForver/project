# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:20:58 2019

@author: qwq
"""

import cv2

knownWidth = 140 # -mm
knownHeight = 61
ratioX = 2.5
ratioY = 3
img = cv2.imread('C:/Users/qwq/Desktop/image/test.jpg')
h, w = img.shape[:2]
x = w/2 - ratioX*knownWidth
y = h/2 - ratioY*knownHeight
x2 = w/2 + ratioX*knownWidth
y2 = h/2 + ratioY*knownHeight
 # Crop from {x, y, w, h } => {0, 0, 300, 400}
crop_img = img[int(y):int(y2),int(x):int(x2)]

while True:
    cv2.imshow("original", img)
    cv2.imshow("cropped", crop_img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
