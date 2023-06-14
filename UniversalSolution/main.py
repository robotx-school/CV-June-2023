import socket
import pickle
import struct
import cv2
import time
import numpy as np

from config import *
from get_image import get_image
from undistort_image import undistort
from warp_field import warp_field
from split_image import split_image
from find_robot import find_robot
from find_robot_battery import find_robot_battery


    

while True:
    frame = get_image(HOST_IP, HOST_PORT)
    undistroted_image = undistort(frame, K, D)
    field_img = warp_field(undistroted_image, ARUCO_DICT)
    image_set = split_image(field_img,image_split_coords)
    robot_right_top, robot_right_bottom = find_robot(image_set['robot_right'])
    robot_left_top, robot_left_bottom = find_robot(image_set['robot_left'])
    right_robot_battery = find_robot_battery(image_set['robot_right'])
    left_robot_battery = find_robot_battery(image_set['robot_left'])
    #field_coord_right_robot_battery =
    #field_coord_left_robot_battery = 

    #mm_coord_right_robot_battery =
    #mm_coord_left_robot_battery =

    #left_manip_coord_right_robot_battery =
    #left_manip_coord_left_robot_battery = 

    #right_manip_coord_right_robot_battery =
    #right_manip_coord_left_robot_battery =

    #is_bat_charged_up =
    #is_bat_charged_down =
    #is_bat_discharged_up =
    #is_bat_discharged_down =

    #координаты АКБ в координатах роботов

    #mega_show_img = get_mega_show()

    #robot_control()
    cv2.imshow("img", image_set['robot_left'])
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        cv2.imwrite(f"images/{time.time()}.jpg", frame)
        print(f"File: images/{time.time()}.jpg saved")
cv2.destroyAllWindows()
