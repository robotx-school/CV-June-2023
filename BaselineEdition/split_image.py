import cv2
import numpy as np

def split_image(img,image_split_coords):
    image_set = {"robot_left":img[0:480,image_split_coords['robot_left_l_x']:image_split_coords['robot_left_r_x']],
                 "robot_right":img[0:480,image_split_coords['robot_right_l_x']:image_split_coords['robot_right_r_x']],
                 "bat_charged_up":img[70:240,550:640],
                 "bat_charged_down":img[200:360, 550:640],
                 "bat_discharged_up":img[70:240, 0:90],
                 "bat_discharged_down":img[200:360, 0:90]}
    return image_set

