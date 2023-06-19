import cv2
import numpy as np

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

HOST_IP = "192.168.2.237"
HOST_PORT = 9988

ROBOT1 = {"ip":"192.168.0.10",
          "acel":0.2,
          "speed":0.4}

ROBOT2 = {"ip":"192.168.0.10",
          "acel":0.2,
          "speed":0.4}

with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())
image_split_coords = {'robot_left_l_x': 90,
                      'robot_left_r_x':320,
                      'robot_right_l_x':320,
                      'robot_right_r_x':550}

robotleft = [
    {"home": {"x": 10, "y": 10, "z": 10, "a": 360, "b": 360, "c": 360},
     "discharged_up": {"x": 10, "y": 10, "z": 10, "a": 360, "b": 360, "c": 360},
     "discharged_down": {"x": 10, "y": 10, "z": 10, "a": 360, "b": 360, "c": 360}}
]
robotright = [
    {"home": {"x": 10, "y": 10, "z": 10, "grip": 360},
     "charged_up": {"x": 10, "y": 10, "z": 10, "grip": 360},
     "charged_down": {"x": 10, "y": 10, "z": 10, "grip": 360}}
]
