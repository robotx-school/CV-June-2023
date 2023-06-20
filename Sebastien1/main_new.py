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
from roboctrl import right_robot_control, left_robot_control
from roboctrl_class import *
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
    
    if robot_right_top is not None:
        visualizer.draw_robot([(330, robot_right_top), (520, robot_right_bottom)])
    if robot_left_top is not None:
        visualizer.draw_robot([(110, robot_left_top), (310, robot_left_bottom)])

    
        
    right_robot_battery = find_robot_battery(image_set['robot_right'],17, ARUCO_DICT)
    left_robot_battery = find_robot_battery(image_set['robot_left'],17, ARUCO_DICT)
    
    if right_robot_battery[0][0] is not None:
        field_coord_right_robot_battery = get_correct_coordinates(right_robot_battery,image_split_coords['robot_right_l_x'])
        mm_coord_right_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img,image_split_coords)[1]),l_cam2map_convert(field_coord_right_robot_battery[0][0]))
        mm_coord_right_robot_battery = fixed_proportion(mm_coord_right_robot_battery, visual_size = [640, 400])
        print("mm_coord_right_robot_battery",mm_coord_right_robot_battery)
        left_manip_coord_right_robot_battery = get_l_manup_cords(mm_coord_right_robot_battery)
        right_manip_coord_right_robot_battery = get_r_manup_cords(mm_coord_right_robot_battery)
        visualizer.draw_marker(mm_coord_right_robot_battery[0],mm_coord_right_robot_battery[1], 17, right_robot_battery[0][1])                                                         
    else:
        print('no right robot')
    

    if left_robot_battery[0][0] is not None:
        field_coord_left_robot_battery = get_correct_coordinates(left_robot_battery,image_split_coords['robot_left_l_x'])
        mm_coord_left_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img,image_split_coords)[0]),l_cam2map_convert(field_coord_left_robot_battery[0][0]))
        #mm_coord_right_robot_battery = fixed_proportion(mm_coord_right_robot_battery, visual_size = [640, 400])
        print("mm_coord_left_robot_battery",mm_coord_left_robot_battery)
        left_manip_coord_left_robot_battery = get_l_manup_cords(mm_coord_left_robot_battery)
        right_manip_coord_left_robot_battery = get_r_manup_cords(mm_coord_left_robot_battery)
        visualizer.draw_marker(mm_coord_left_robot_battery[0],mm_coord_left_robot_battery[1], 17, left_robot_battery[0][1])                                                         
    else:
        print('no left robot')
        
    cv2.imshow("Visualization", visualizer.image)
    cv2.imshow("field_img",field_img)
    
    is_bat_charged_up = check_marker(image_set['bat_charged_up'])
    is_bat_charged_down = check_marker(image_set['bat_charged_down'])
    is_bat_discharged_up = check_marker(image_set['bat_discharged_up'])
    is_bat_discharged_down = check_marker(image_set['bat_discharged_down'])
    

    print("angle",right_robot_battery[0][1])
    print("robot right top",robot_right_top)
    ctrl = roboctrl(right_robot_battery, left_robot_battery)
    ctrl.right_robot_control()
    ctrl.left_robot_control()
    '''
    if __name__ == '__main__':
        ctrl = roboctrl(right_robot_battery, left_robot_battery)
        ctrl.right_robot_control()
        ctrl.left_robot_control()
    '''    
    #right_robot_control(right_robot_battery)
    #left_robot_control(left_robot_battery)
    
        









        













    #time.sleep(2)
    #robot.movel([0.021, -0.39, 0.18, rx, ry, 0] , 0.1 , 0.2, wait = True)
    #time.sleep(2)
    #aruco_in_robotic_coords = get_l_manup_cords(mm_coord_right_robot_battery)
    #robot.movel([aruco_in_robotic_coords[0], aruco_in_robotic_coords[1], 0.30, rx, ry, 0] , 0.1 , 0.2, wait = True)
    #except:
    #    print('cannot turn roboot')
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        cv2.imwrite(f"images/{time.time()}.jpg", frame)
        print(f"File: images/{time.time()}.jpg saved")
cv2.destroyAllWindows()
