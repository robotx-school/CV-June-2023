import socket
import pickle
import struct
import cv2
import time
import numpy as np
from threading import Thread

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

visualizer = Visualize()
p =None
def potok(t):
    for i in range(t):
        time.sleep(1)
        print(i)


def save_image_set(image_set_dict):
    for name, image in image_set_dict.items():
        cv2.imwrite(f"images/{name}.jpg", image)


def show_all(camera_image, field_img, visualizer_image):
    camera_image = cv2.resize(camera_image, (320, 240))
    field_img = cv2.resize(field_img, (320, 240))
    visualizer_image = cv2.resize(visualizer_image, (640, 480))
    visualizer_image = cv2.cvtColor(visualizer_image, cv2.COLOR_BGRA2BGR)
    top = cv2.hconcat((camera_image, field_img))
    top = cv2.resize(top, (640, 240))
    all = cv2.vconcat((top, visualizer_image))
    return all


while True:
    visualizer.update()  # очищаем поле визуализатора
    frame = get_image(HOST_IP, HOST_PORT)  # получаем изображение с камеры
    undistroted_image = undistort(frame, K, D)  # выпрямляем изображение
    field_img = warp_field(undistroted_image, ARUCO_DICT)  # получаем поле
    image_set = split_image(field_img, image_split_coords)  # разделяем поле на части
    save_image_set(image_set)  # в папку images сохраняем части поля

    robot_right_top, robot_right_bottom = find_robot(image_set['robot_right'].copy())
    # находим координаты робота в правой части поля
    robot_left_top, robot_left_bottom = find_robot(image_set['robot_left'].copy())
    # находим координаты робота в правой части поля
    if robot_right_top is not None:
        visualizer.draw_robot([(330, robot_right_top), (520, robot_right_bottom)])
    if robot_left_top is not None:
        visualizer.draw_robot([(110, robot_left_top), (310, robot_left_bottom)])
    # рисуем робота

    right_robot_battery = find_robot_battery(image_set['robot_right'], 17, ARUCO_DICT)
    left_robot_battery = find_robot_battery(image_set['robot_left'], 17, ARUCO_DICT)

    if right_robot_battery[0][0] is not None:
        field_coord_right_robot_battery = get_correct_coordinates(right_robot_battery,
                                                                  image_split_coords['robot_right_l_x'])

        mm_coord_right_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img, image_split_coords)[1]),
                                                    l_cam2map_convert(field_coord_right_robot_battery[0][0]))
        mm_coord_right_robot_battery = fixed_proportion(mm_coord_right_robot_battery, visual_size=[640, 400])

        left_manip_coord_right_robot_battery = get_l_manup_cords(mm_coord_right_robot_battery)
        right_manip_coord_right_robot_battery = get_r_manup_cords(mm_coord_right_robot_battery)
        visualizer.draw_marker(mm_coord_right_robot_battery[0], mm_coord_right_robot_battery[1], 17,
                               right_robot_battery[0][1])
    else:
        print('no right robot')

    if left_robot_battery[0][0] is not None:
        field_coord_left_robot_battery = get_correct_coordinates(left_robot_battery,
                                                                 image_split_coords['robot_left_l_x'])
        mm_coord_left_robot_battery = list_average(e_cam2map_convert(e_cam2map_cut(field_img, image_split_coords)[0]),
                                                   l_cam2map_convert(field_coord_left_robot_battery[0][0]))
        left_manip_coord_left_robot_battery = get_l_manup_cords(mm_coord_left_robot_battery)
        right_manip_coord_left_robot_battery = get_r_manup_cords(mm_coord_left_robot_battery)
        visualizer.draw_marker(mm_coord_left_robot_battery[0], mm_coord_left_robot_battery[1], 17,
                               left_robot_battery[0][1])
    else:
        print('no left robot')

    is_bat_charged_up = check_marker(image_set['bat_charged_up'])
    is_bat_charged_down = check_marker(image_set['bat_charged_down'])
    is_bat_discharged_up = check_marker(image_set['bat_discharged_up'])
    is_bat_discharged_down = check_marker(image_set['bat_discharged_down'])

    visualizer.draw_battery(is_bat_charged_up, is_bat_charged_down, is_bat_discharged_up, is_bat_discharged_down)
    result_img = show_all(frame, field_img, visualizer.image)
    cv2.imshow("Visualization", result_img)


    print("p=",p if p is None else p.is_alive())
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == 32:
        p = Thread(target=potok, args=(5,))
        p.start()
        cv2.imwrite(f"images/{time.time()}.jpg", frame)
        print(f"File: images/{time.time()}.jpg saved")
cv2.destroyAllWindows()
