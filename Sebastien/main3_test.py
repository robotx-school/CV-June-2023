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
h_min = (20, 140, 173)# red minimum value
h_max = (255, 255, 255)# red maximum value
numba = 0
save_h = np.array([])
use = 0
xtra = 100
x_mm = 0#600mm
y_mm = 0#400mm


while True:
    
    field_copy = cv2.resize(field,(640, 480)) # creates copy of field
    frame = get_image() # get frame from camera
    frame = undistort(frame) # fix camera distortion
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert frame to color hsv format
    h_ = warp_da(frame) # get coordinates of 4 corners and warp perspective

    h, w, _ = frame.shape # get the shape of the frame
    res_img = cv2.warpPerspective(frame, h_, (w, h)) # address warp_da to res_img

    left  = res_img[0:480, 0 + xtra:320]
    right = res_img[0:480, 320:640-xtra]
    test  = res_img[0:480, 0:320]
    img_bin_r = cv2.inRange(right, h_min, h_max) # cropped black and white version
    bitwiseNot_r = cv2.bitwise_not(img_bin_r) # invert img_bin
    summa = np.sum(bitwiseNot_r, axis=1) # creates an array of sum values
    dafk = np.where(summa>10000) # coordinates of values over 10000
    
    if len(dafk[0])>1: # if at least 2 red pixels exist

        cv2.rectangle(field_copy,
                      (320,dafk[0][0]),
                      (520,dafk[0][len(dafk[0])-1]),
                      (0,0,255), -1)

    # if aruco found returns angle, x, y. if not found returns None,None,None

    angle_r, dot_x_r, dot_y_r = find_aruco_rotation(right)
    angle_test, dot_x_test, dot_y_test = find_aruco_rotation(test)
    
    if angle_r is not None: # if aruco found
        '''
        if 0<=abs(angle_r)<=90:
            print('angle: ',abs(angle_r))
        else:
            print('angle: ',abs(angle_r)-90)
        '''    
        
        
        cv2.circle(field_copy, (dot_x_r+320, dot_y_r), 80, (255,255,255), thickness=-1)#draws a circle in the center of the aruco marker
        field_copy = insert_rotated_image(field_copy,aruco,angle_r,(dot_y_r, dot_x_r+320))
        get_robot_c = get_robot_coords(((dot_x_r+320,dot_y_r),))

        
        x_mm = 600*(dot_x_r+320)/640#600mm
        y_mm = 400*(dot_y_r)/480#400mm

        
        field_copy = cv2.putText(field_copy, 'x mm: '+str(x_mm),
                                 (dot_x_r+160, dot_y_r),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (0,0,0), 1, cv2.LINE_AA)

        
        field_copy = cv2.putText(field_copy, 'y mm: '+str(y_mm),
                                 (dot_x_r+160, dot_y_r+20),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (0,0,0), 1, cv2.LINE_AA)



        robot_coords = get_robot_coords(((x_mm,y_mm),))
        field_copy = cv2.putText(field_copy, str(robot_coords),
                                 (dot_x_r+160, dot_y_r+40),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (0,0,0), 1, cv2.LINE_AA)




    if angle_test is not None:
        print()
        x_mm_test = 600*(dot_x_test)/640#600mm
        y_mm_test = 400*(dot_y_test)/480#400mm
        field_copy = cv2.putText(field_copy, str(x_mm_test)+' '+str(y_mm_test),
                                 (dot_x_test+160, dot_y_test+80),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (0,0,100), 1, cv2.LINE_AA)
        print(dot_x_test, dot_y_test)
        print(x_mm_test,y_mm_test)
        print(get_robot_coords([x_mm_test,y_mm_test]))
        print()

        '''
        robot_coords_test = get_robot_coords(((x_mm_test,y_mm_test),))
        field_copy = cv2.putText(field_copy, str(robot_coords_test),
                                 (dot_x_test+160, dot_y_test+80),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (0,0,100), 1, cv2.LINE_AA)
        '''


    # creates windows    
    cv2.imshow('warp',res_img)
    cv2.imshow("field", field_copy)
    #cv2.imshow("img", frame)
    #cv2.imshow('l', left)
    #cv2.imshow('r', right)

    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break

    
cv2.destroyAllWindows()
