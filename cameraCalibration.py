# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 00:56:49 2019

@author: qwq

"""

### problem unsolved: roi = [0,0,0,0]
### ref: http://answers.opencv.org/question/102485/problem-with-getoptimalnewcameramatrix/
### just repeat calibration

import numpy as np
import cv2
import glob

# termination criteria

chrow = 6
chcol = 4
dimension = 29 #-mm

workingFolder = "C:/Users/qwq/Desktop/image/"
imageType = "jpg"

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chrow*chcol,3), np.float32)
objp[:,:2] = np.mgrid[0:chcol,0:chrow].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Find the images files
filename = workingFolder + "*." + imageType
images = glob.glob(filename)

print("Find {} images".format(len(images)))

nPattern = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (chcol,chrow),None)
  
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("Find the image: {}".format(fname))
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (chcol,chrow), corners2,ret)
        nPattern += 1
        #while True:
         #   cv2.imshow('img',img)
          #  if cv2.waitKey(1) & 0xFF == ord('q'):
           #     break
cv2.destroyAllWindows()

print("Find {} good images to calibrate".format(nPattern))
           
rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
       

#undistort an image
img = cv2.imread('C:/Users/qwq/Desktop/image/image7.jpg')
h, w = img.shape[:2]
#newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

#mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,mtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

#crop the image
#x,y,w,h = roi
#dst = dst[y:y+h, x:x+w]
cv2.imwrite('C:/Users/qwq/Desktop/image/calibration7.jpg',dst)
print("well done")

#while True:
#    cv2.imshow('calibration',dst)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
cv2.destroyAllWindows()

#-------- Save result
filename = workingFolder + "cameraMatrix.txt"
np.savetxt(filename, mtx, delimiter = ',' )
filename = workingFolder + "/cameraDistortion.txt"
np.savetxt(filename, dist, delimiter = ',')

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i],mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
    
print ("total error: {}".format( mean_error/len(objpoints)))






