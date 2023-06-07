import cv2
import numpy as np
import os
import glob


with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())

def undistort(img):
    DIM = img.shape[:2][::-1]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img[::]

image = cv2.imread("images/run.jpg")
image = undistort(image)
cv2.imshow('abc',image)

