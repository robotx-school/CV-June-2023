import socket
import pickle
import struct
import cv2
import time
import numpy as np
import urx
import math3d as m3d
from config import *
from get_image import get_image
from undistort_image import undistort
from warp_field import warp_field
from split_image import split_image
from find_robot import find_robot
from find_robot_battery import find_robot_battery
from check_marker import check_marker
from e_cam2map_convert import e_cam2map_convert
from l_cam2map_convert import l_cam2map_convert
from list_average import list_average
from get_manup_coords import get_l_manup_cords, get_r_manup_cords
from convert_crop_coords_to_field_coords import get_correct_coordinates
from check_marker import check_marker
from visualize import Visualize
from e_cam2map_cut import e_cam2map_cut
from fixed_proportion import fixed_proportion
from get_manup_coords import get_l_manup_cords
from angle_gipper import *
import numpy as np
import math
import urx, time
import numpy as np
import math3d as m3d
import time

visualizer = Visualize()

try:
    robot = urx.Robot('192.168.2.65')
    from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
    robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
except Exception as e:
    print('robot connection error',e)

acc = 0.2

while True:
    visualizer.update()
    frame = get_image(HOST_IP, HOST_PORT)
    undistroted_image = undistort(frame, K, D)
    field_img = warp_field(undistroted_image, ARUCO_DICT)
    image_set = split_image(field_img,image_split_coords)
    robot_right_top, robot_right_bottom = find_robot(image_set['robot_right'].copy())
    robot_left_top, robot_left_bottom = find_robot(image_set['robot_left'].copy())
    print(image_set)
    if robot_right_top is not None:
        visualizer.draw_robot([(330, robot_right_top), (520, robot_right_bottom)])
    if robot_left_top is not None:
        visualizer.draw_robot([(110, robot_left_top), (310, robot_left_bottom)])

    
        

