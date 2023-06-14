#Sebastien
#imports libraries
import cv2
import time
import os
import numpy as np
import math
import cv2.aruco as aruco
from visualization import *
from get_img import *
from aruco_angle import *
from insert_Image import *
from manipulate_img import *
from get_robot_coords import *
# this code is for the rightside, but you can easily change it
def visualization(field_copy,dot_x,dot_y,aruco,angle_r):
    
    field_copy = insert_rotated_image(field_copy,aruco,angle_r,(dot_y_r, dot_x_r+320)) # puts aruco marker
    get_robot_c = get_robot_coords([dot_x_r+320,dot_y_r])#gets cooordinates 320 is the middle of the field


    x_mm = 590*(dot_x_r+320)/640 + 5#600mm
    y_mm = 390*(dot_y_r)/480     + 5#400mm


    field_copy = cv2.putText(field_copy, 'x mm: '+str(x_mm),
                             (dot_x_r+160, dot_y_r),
                             cv2.FONT_HERSHEY_SIMPLEX,
                             0.5, (0,0,0), 1, cv2.LINE_AA)


    field_copy = cv2.putText(field_copy, 'y mm: '+str(y_mm),
                             (dot_x_r+160, dot_y_r+20),
                             cv2.FONT_HERSHEY_SIMPLEX,
                             0.5, (0,0,0), 1, cv2.LINE_AA)



    robot_coords = get_robot_coords([x_mm,y_mm])
    field_copy = cv2.putText(field_copy, str(robot_coords),
                             (dot_x_r+160, dot_y_r+40),
                             cv2.FONT_HERSHEY_SIMPLEX,
                             0.5, (0,0,0), 1, cv2.LINE_AA)
    return field_copy
