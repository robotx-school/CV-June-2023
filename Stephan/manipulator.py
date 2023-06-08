import urx
import time
import numpy as np
import math3d as m3d
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import logging


class UR3Client:
    def __init__(self, id: str, x_min: float = -0.460, acc: float = .1, speed: float = 0.1) -> None:
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
        # Offsets
        self.offset_x = -75
        self.offset_y = 200
        try:
            self.robot = urx.Robot('192.168.2.65')
            self.robotiqgrip = Robotiq_Two_Finger_Gripper(self.robot)
        except Exception as e:
            logging.error(f"Robot connection error: {e}")
        with open(f"./positions/home_{id}.txt") as fd:
            self.home_position = eval(fd.read())
        logging.info(f"Robot {id} home pose is: {self.home_position}")
        with open(f"./positions/cube_static_{id}.txt") as fd:
            self.static_cube_position = eval(fd.read())
        logging.info(f"Robot {id} static cube pose is: {self.home_position}")

    def go(self, coord):
        # x_min = -0.460
        # x_max = -0.175
        # y_min = -0.21
        # y_max = 0.21
        if self.robot:
            x = coord[0] / 1000
            y = coord[1] / 1000
            y -= 0.02
            logging.info(f"Trying to move to {x}; {y}")
            if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
                print('go')
                if 0:
                    state = self.robot.getl()
                    print(state)
                    # robot.movel([-0.21, 0.25, 0.2, 0.00, 3.14, 0.0],
                    #             acc=acc, vel=speed, wait=True)
                    # time.sleep(self.time_delay)
            else:
                logging.error("Bad coords protection error; can't move")
        else:
            logging.error("Robot not connected")

    def home(self):
        self.robot.movel(self.home_position, acc=self.acc, vel=self.speed, wait=True)

    def cube_static(self):
        self.robot.movel(self.static_cube_position, acc=self.acc, vel=self.speed, wait=True)

    def get_robot_coords(self, coords):
        # offset_x = -143
        # offset_y = 200
        robot_coords_res = []
        for coord in [coords]:
            x_r = coord[0] + self.offset_x
            y_r = coord[1] + self.offset_y
            x_r, y_r = -y_r, -x_r
            robot_coords_res.append((x_r / 1000, y_r / 1000))
        return robot_coords_res


if __name__ == "__main__":
    robot = UR3Client("discharged")
    res = robot.get_robot_coords((401, 126))
    print(res)
    
