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
# PUT ARUCO MARKER ON CHARGING ZONE
try:
    robot = urx.Robot('192.168.2.65')
    from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
    robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
except Exception as e:
    print('robot connection error',e)

acc = 0.2
def right_robot_control(right_robot_battery):
        if right_robot_battery is not [[6*None]]:
                lx, ly, lz = angle_gripper(right_robot_battery[0][1])
                robot.movel([get_l_manup_cords(mm_coord_right_robot_battery)[0],
                             get_l_manup_cords(mm_coord_right_robot_battery)[1], 0.30,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                time.sleep(2)
                robot.movel([get_l_manup_cords(mm_coord_right_robot_battery)[0],
                             get_l_manup_cords(mm_coord_right_robot_battery)[1], 0.10,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(100)
                time.sleep(2)
                robot.movel([0.04296983079787211, -0.16314794573917965,
                             0.1730807039791688, -2.1223205010505057,
                             2.2437465531073446, 0.04561178965761669],
                            0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(0)
                time.sleep(2)
                # pick up charged marker and place on robot
                lx, ly, lz = angle_gripper(right_robot_battery[0][1])
                robot.mover([0.1108634530794939, -0.08892304885884085, 0.3385760801340761,
                              2.156131292945468, 2.207640399842002, -0.023220213819268334],
                             0.1 , 0.2, wait = True)
                time.sleep(2)
                robotiqgrip.gripper_action(150)
                robot.mover([get_r_manup_cords(mm_coord_right_robot_battery)[0],
                             get_r_manup_cords(mm_coord_right_robot_battery)[1], 0.30,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                time.sleep(2)
                robot.mover([get_r_manup_cords(mm_coord_right_robot_battery)[0], 
                             get_l_manup_cords(mm_coord_right_robot_battery)[1], 0.10,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(0)
                robot.mover([0.1108634530794939, -0.08892304885884085, 0.3385760801340761,
                              2.156131292945468, 2.207640399842002, -0.023220213819268334],
                             0.1 , 0.2, wait = True)






def left_robot_control(left_robot_battery):
        if left_robot_battery is not [[6*None]]:
                lx, ly, lz = angle_gripper(left_robot_battery[0][1])
                robot.movel([get_l_manup_cords(mm_coord_left_robot_battery)[0],
                             get_l_manup_cords(mm_coord_left_robot_battery)[1], 0.30,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                time.sleep(2)
                robot.movel([get_l_manup_cords(mm_coord_left_robot_battery)[0],
                             get_l_manup_cords(mm_coord_left_robot_battery)[1], 0.10,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(100)
                time.sleep(2)
                robot.movel([0.04296983079787211, -0.16314794573917965,
                             0.1730807039791688, -2.1223205010505057,
                             2.2437465531073446, 0.04561178965761669],
                            0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(0)
                time.sleep(2)
                # pick up charged marker and place on robot
                lx, ly, lz = angle_gripper(left_robot_battery[0][1])
                robot.mover([0.1108634530794939, -0.08892304885884085, 0.3385760801340761,
                              2.156131292945468, 2.207640399842002, -0.023220213819268334],
                             0.1 , 0.2, wait = True)
                time.sleep(2)
                robotiqgrip.gripper_action(150)
                robot.mover([get_r_manup_cords(mm_coord_left_robot_battery)[0],
                             get_l_manup_cords(mm_coord_left_robot_battery)[1], 0.30,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                time.sleep(2)
                robot.mover([get_r_manup_cords(mm_coord_left_robot_battery)[0], 
                             get_l_manup_cords(mm_coord_left_robot_battery)[1], 0.10,
                             lx, ly, 0] , 0.1 , 0.2, wait = True)
                robotiqgrip.gripper_action(0)
                robot.mover([0.1108634530794939, -0.08892304885884085, 0.3385760801340761,
                              2.156131292945468, 2.207640399842002, -0.023220213819268334],
                             0.1 , 0.2, wait = True)


