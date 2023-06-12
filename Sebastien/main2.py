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
#from robot_control import *


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

xtra=100
x_mm = 0#600mm
y_mm = 0#400mm
while True:
    field_copy = cv2.resize(field,(640, 480)) # creates copy of field
    frame = get_image() # get frame from camera
    frame = undistort(frame) # fix camera distortion
    #frame = cv2.flip(frame, 1)#### ### ### ### ### ### ### ####################################
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert frame to color hsv format
    h_ = warp_da(frame) # get coordinates of 4 corners and warp perspective
    h, w, _ = frame.shape # get the shape of the frame
    res_img = cv2.warpPerspective(frame, h_, (w,h)) # address warp_da to res_img
    left  = res_img[0:480, 0+xtra:320]
    right = res_img[0:480, 320:640-xtra]

    cv2.imshow('l', left)
    cv2.imshow('r', right)
    print('res_shape',res_img.shape)
    
    img_bin_r = cv2.inRange(right, h_min, h_max) # cropped black and white version
    bitwiseNot_r = cv2.bitwise_not(img_bin_r) # invert img_bin
    cv2.imshow('ChargingZoneSector1', img_bin_r) # show img_bin
    cv2.imshow('bitwiseNot', bitwiseNot_r) # show bitwiseNot
    summa = np.sum(bitwiseNot_r, axis=1) # creates an array of sum values
    print("SUMMA IS :",summa) # prints summa
    dafk = np.where(summa>10000) # coordinates of values over 10000
    print("DAFK IS: ",len(dafk[0])) # prints dafk
    if len(dafk[0])>1: # if at least 2 red pixels exist
        '''
        cv2.rectangle(res_img, # visualize rectangle on display
                      (100,dafk[0][0]), 
                      (310,dafk[0][len(dafk[0])-1]),
                      (0,0,255), -1)
        '''
        cv2.rectangle(field_copy,
                      (320,dafk[0][0]),
                      (520,dafk[0][len(dafk[0])-1]),
                      (0,0,255), -1)

    # if aruco found returns angle, x, y. if not found returns None,None,None

    '''
    angle_l, dot_x_l, dot_y_l = find_aruco_rotation(left)
    
    if angle_l is not None: # if aruco found
        if 0<=abs(angle_l)<=90:
            print('angle: ',abs(angle_l))
        else:
            print('angle: ',abs(angle_l)-90)
        cv2.circle(field_copy, (dot_x_l+xtra, dot_y_l), 10, (255,255,255), thickness=-1)#draws a circle in the center of the aruco marker
        field_copy = insert_rotated_image(field_copy,aruco,angle,(dot_y_l, dot_x_l+xtra))
        get_robot_c = get_robot_coords(((dot_x_l+xtra,dot_y_l),))
        print(get_robot_c)


    '''
    angle_r, dot_x_r, dot_y_r = find_aruco_rotation(right)
    
    if angle_r is not None: # if aruco found
        if 0<=abs(angle_r)<=90:
            print('angle: ',abs(angle_r))
        else:
            print('angle: ',abs(angle_r)-90)
        cv2.circle(field_copy, (dot_x_r+320, dot_y_r), 80, (255,255,255), thickness=-1)#draws a circle in the center of the aruco marker
        field_copy = insert_rotated_image(field_copy,aruco,angle_r,(dot_y_r, dot_x_r+320))
        get_robot_c = get_robot_coords(((dot_x_r+320,dot_y_r),))
        print(get_robot_c)
        x_mm = 600*(dot_x_r+320)/640#600mm
        y_mm = 400*(480-dot_y_r)/480#400mm
        print('x_mm',x_mm)
        print('y_mm',y_mm)
        test = get_robot_coords(((x_mm,y_mm),))
        print("test",test)
    # creates windows    
    cv2.imshow('warp',res_img)
    cv2.imshow("field", field_copy)
    cv2.imshow("img", frame)


    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break

    
cv2.destroyAllWindows()
