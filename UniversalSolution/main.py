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
from check_marker import check_marker
from e_cam2map_convert import e_cam2map_convert
from l_cam2map_convert import l_cam2map_convert
from list_average import list_average
from get_manup_coords import get_l_manup_cords, get_r_manup_cords
from convert_crop_coords_to_field_coords import get_correct_coordinates
from check_marker import check_marker
from visualize import Visualize
from e_cam2map_cut import e_cam2map_cut



visualizer = Visualize()

while True:
    frame = get_image(HOST_IP, HOST_PORT)
    undistroted_image = undistort(frame, K, D)
    field_img = warp_field(undistroted_image, ARUCO_DICT)
    image_set = split_image(field_img,image_split_coords)
    robot_right_top, robot_right_bottom = find_robot(image_set['robot_right'])
    robot_left_top, robot_left_bottom = find_robot(image_set['robot_left'])

    right_robot_battery = find_robot_battery(image_set['robot_right'],17, ARUCO_DICT)
    left_robot_battery = find_robot_battery(image_set['robot_left'],17, ARUCO_DICT)


    if right_robot_battery[0][0] is not None:
        field_coord_right_robot_battery = get_correct_coordinates(right_robot_battery,image_split_coords['robot_right_l_x'])
        mm_coord_right_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img,image_split_coords)[0]),l_cam2map_convert(field_coord_right_robot_battery))
        left_manip_coord_right_robot_battery = get_l_manup_cords(mm_coord_right_robot_battery)
        right_manip_coord_right_robot_battery = get_r_manup_cords(mm_coord_right_robot_battery)
    else:
        print('no right robot')
    

    if left_robot_battery[0][0] is not None:
        field_coord_left_robot_battery = get_correct_coordinates(left_robot_battery,image_split_coords['robot_left_l_x'])
        mm_coord_left_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img,image_split_coords)[1]),l_cam2map_convert(field_coord_left_robot_battery))
        left_manip_coord_left_robot_battery = get_l_manup_cords(mm_coord_left_robot_battery)
        right_manip_coord_left_robot_battery = get_r_manup_cords(mm_coord_left_robot_battery)
    else:
        print('no left robot')


    
    is_bat_charged_up = check_marker(image_set['bat_charged_up'])
    is_bat_charged_down = check_marker(image_set['bat_charged_down'])
    is_bat_discharged_up = check_marker(image_set['bat_discharged_up'])
    is_bat_discharged_down = check_marker(image_set['bat_discharged_down'])

    #robot_control() Stas
    visualizer.update()
    visualizer.draw_robot([(100, 100), (150, 150)])  
    visualizer.draw_marker(100, 100, 17, 45)                                                         
    cv2.imshow("Visualization", visualizer.image)
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        cv2.imwrite(f"images/{time.time()}.jpg", frame)
        print(f"File: images/{time.time()}.jpg saved")
cv2.destroyAllWindows()
