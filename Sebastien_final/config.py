import cv2
import numpy as np

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

HOST_IP = "192.168.0.222" #"127.0.0.1"
HOST_PORT = 9988

with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())
image_split_coords = {'robot_left_l_x': 90,
                      'robot_left_r_x': 320,
                      'robot_right_l_x': 320,
                      'robot_right_r_x': 550}

l_manip_positions = {'home': [0.113, -0.069, 0.374, 90],
                     'pre_home': [0.024, -0.189, 0.368, 90],
                     'up_discharged': [0.045, -0.152, 0.186, 90],
                     'pre_up_discharged': [0.045, -0.152, 0.216, 90],
                     'down_discharged': [-0.055, -0.145, 0.186, 0],
                     'pre_down_discharged': [-0.057, -0.145, 0.216, 0],
                     'center': [-0.001, -0.38, 0.186, 45],
                     'pre_center': [-0.001, -0.38, 0.216, 45],
                     }

r_manip_positions = {'home': [-0.077, -0.111, 0.257, 90],
                     'pre_home': [-0.203, -0.055, 0.240, 90],
                     'up_charged': [-0.155, 0.054, 0.031, 0],
                     'pre_up_charged': [-0.155, 0.054, 0.054, 0],
                     'down_charged': [-0.153, -0.047, 0.031, 90],
                     'pre_down_charged': [-0.153, -0.047, 0.054, 90],
                     'center': [-0.375, -0.001, 0.031, 45],
                     'pre_center': [-0.375, -0.001, 0.054, 45],
                     }


