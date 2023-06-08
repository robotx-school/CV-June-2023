# import all libraries
import cv2
import time
import os
import numpy as np
import math
from manipulate_img import *
from get_img import *
from aruco_angle import *
from insert_Image import *
import cv2.aruco as aruco
from get_robot_coords import *
from robot_control import *


field = cv2.imread('field.jpg')# imports field.jpg
aruco = create_aruco_marker(17)# creates aruco
h_min=(0,140,173)# red minimum value
h_max=(255,255,255)# red maximum value
numba=0
save_h = np.array([])
use=0


with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())


while True:
    field_copy = cv2.resize(field,(640, 480)) # creates copy of field
    frame = get_image() # get frame from camera
    frame = undistort(frame) # fix camera distortion
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert frame to color hsv format
    h_ = warp_da(frame) # get coordinates of 4 corners and warp perspective
    h, w, _ = frame.shape # get the shape of the frame
    res_img = cv2.warpPerspective(frame, h_, (w,h)) # address warp_da to res_img
    img_bin = cv2.inRange(res_img[0:480, 90:300], h_min, h_max) # cropped black and white version
    bitwiseNot = cv2.bitwise_not(img_bin) # invert img_bin
    cv2.imshow('ChargingZoneSector1', img_bin) # show img_bin
    cv2.imshow('bitwiseNot', bitwiseNot) # show bitwiseNot
    summa = np.sum(bitwiseNot, axis=1) # creates an array of sum values
    print("SUMMA IS :",summa) # prints summa
    dafk = np.where(summa>10000) # coordinates of values over 10000
    print("DAFK IS: ",len(dafk[0])) # prints dafk
    if len(dafk[0])>1: # if at least 2 red pixels exist
        cv2.rectangle(res_img, # visualize rectangle on display
                      (100,dafk[0][0]), 
                      (310,dafk[0][len(dafk[0])-1]),
                      (0,0,255), -1)
        cv2.rectangle(field_copy,
                      (100,dafk[0][0]),
                      (310,dafk[0][len(dafk[0])-1]),
                      (0,0,255), -1)





    # if aruco found returns angle, x, y. if not found returns None,None,None
    angle, dot_x, dot_y = find_aruco_rotation(res_img)
    
    if angle is not None: # if aruco found
        if 0<=abs(angle)<=90:
            print('angle: ',abs(angle))
        else:
            print('angle: ',abs(angle)-90)
    
    
    
        cv2.circle(field_copy, (dot_x, dot_y), 10, (255,255,255), thickness=-1)#draws a circle in the center of the aruco marker
        field_copy = insert_rotated_image(field_copy,aruco,angle,(dot_y, dot_x))
        get_robot_c = get_robot_coords(((dot_x,dot_y),))
        print(get_robot_c)


    # creates windows    
    cv2.imshow('warp',res_img)
    cv2.imshow("field", field_copy)
    cv2.imshow("img", frame)


    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break

    
cv2.destroyAllWindows()
