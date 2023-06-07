import urx
import time
import numpy as np
import math3d as m3d
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import logging

class UR3Client:
    def __init__(self, x_min: float = -0.460, acc: float = .2, speed: float = 0.2) -> None:
        self.x_min = x_min
        self.x_max = -0.175
        self.y_min = -0.21
        self.y_max = 0.21
        self.time_delay = 0.1
        self.acc = acc
        self.speed = speed
        # Try to connect to robot and init gripper
        # If fail we will get None in robot and robotiqgrip
        self.robot = None
        self.robotiqgrip = None
        try:
            self.robot = urx.Robot('192.168.137.60')
            self.robotiqgrip = Robotiq_Two_Finger_Gripper(self.robot)
        except Exception as e:
            logging.error(f"Robot connection error: {e}")



    def go_to(self):
        pass

    def robot_go(self, coord, color):
        dest = {'orange': (-0.314, 0.27),
                'green': (-0.169, 0.3),
                'yellow': (-0.023, 0.3)}
        # x_min = -0.460
        # x_max = -0.175
        # y_min = -0.21
        # y_max = 0.21

        x = coord[0] / 1000
        y = coord[1] / 1000
        y -= 0.02
        print(x, y)
        if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
            print('go')
            if 0:
                state = robot.getl()
                print(state)
                # robot.movel([-0.21, 0.25, 0.2, 0.00, 3.14, 0.0],
                #             acc=acc, vel=speed, wait=True)
                # time.sleep(time_delay)
                # robot.movel([x, y, 0.1, 0.00, 3.14, 0.0],
                #             acc=acc, vel=speed, wait=True)
                # time.sleep(time_delay)
                # robot.movel([x, y, 0.02, 0.00, 3.14, 0.0],
                #             acc=acc, vel=speed, wait=True)
                # time.sleep(time_delay)
                # robotiqgrip.gripper_action(150)

                # robot.movel([dest[color][0], dest[color][1], 0.2,
                #             0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
                # robot.movel([dest[color][0], dest[color][1], 0.12,
                #             0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
                # robotiqgrip.gripper_action(0)
                # robot.movel([dest[color][0], dest[color][1], 0.2,
                #             0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)

                # # home
                # robot.movel([-0.21, 0.25, 0.2, 0.00, 3.14, 0.0],
                #             acc=acc, vel=speed, wait=True)
                time.sleep(self.time_delay)
            """
            robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
            robotiqgrip.gripper_action(0)
            time.sleep(1)
            robot.movel([x, y, 0.1, 0.00, 3.14, 0.0] , 0.3 , 0.2, wait = True)
            time.sleep(1)
            robot.movel([x, y, 0.03, 0.00, 3.14, 0.0] , 0.3 , 0.2, wait = True)
            time.sleep(1)
            robotiqgrip.gripper_action(200)
            time.sleep(1)
            robot.movel([x, y, 0.1, 0.00, 3.14, 0.0] , 0.3 , 0.2, wait = True)
            time.sleep(1)
            robot.movel([x, 0.2, 0.1, 0.00, 3.14, 0.0] , 0.3 , 0.2, wait = True)
            robotiqgrip.gripper_action(0)
            time.sleep(1)
            #go_home
            robot.movel([0.1, 0.25, 0.3, 0.00, 3.14, 0.0] , 0.3 , 0.2, wait = True)
            """
        else:
            print('coord error')

    def get_left_robot_coords(self, coords):
        offset_x = -143
        offset_y = 200
        robot_coords_res = []
        for coord in coords:
            x_r = coord[0] + offset_x
            y_r = coord[1] + offset_y
            x_r, y_r = -y_r, x_r
            robot_coords_res.append((x_r, y_r))
        return robot_coords_res

    def get_right_robot_coords(self, coords):
        offset_x = -143
        offset_y = 200
        robot_coords_res = []
        for coord in coords:
            x_r = coord[0] + offset_x
            y_r = coord[1] + offset_y
            x_r, y_r = -y_r, x_r
            robot_coords_res.append((x_r, y_r))
        return robot_coords_res
