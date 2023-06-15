import cv2
import numpy as np

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

HOST_IP = "192.168.0.222"
HOST_PORT = 9988

with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())
image_split_coords = {'robot_left_l_x': 90,
                      'robot_left_r_x':320,
                      'robot_right_l_x':320,
                      'robot_right_r_x':550}
