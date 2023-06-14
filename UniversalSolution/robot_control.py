from get_robot_coords import get_l_robot_cords, get_r_robot_cords
from config import *
import urx, time
import numpy as np
import math3d as m3d


class Manipulator():
    def __init__(self, ip: str, acceleration: int, speed: int):
        """

        :param ip: IP манипулятора
        :param acceleration: ускорение движения манипулятора
        :param speed: скорость до которой разгоняется манипулятор
        """
        self.ip = ip
        self.conn = False
        self.robot = None
        self.griper = None
        self.acc = acceleration
        self.speed = speed

    def __check_connection__(self) -> str:
        try:
            robot = urx.Robot(self.ip)
            from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

            robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
            try:
                state = robot.getl()
                return "sucses"
            except:
                return "ERROR: GetlERROR"

        except Exception as e:
            ret = 'ERROR: ' + e
            return ret

    def connect(self) -> str:
        con = self.__check_connection__()
        if con != "sucses":
            return con
        else:
            from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
            self.robot = urx.Robot(self.ip)
            self.griper = Robotiq_Two_Finger_Gripper(self.robot)

    def move(self, x: float, y: float, z: float, ang1: float, ang2: float, ang3: float):
        """

        :param x: занчение x куда приехать
        :param y: занчение y куда приехать
        :param z: занчение z куда приехать
        :param ang1: значение 1ого угла руки
        :param ang2: значение 2ого угла руки
        :param ang3: значение 3ого угла руки
        """
        self.robot.movel([x, y, z, ang1, ang2, ang3], acc=self.acc, vel=self.speed, wait=True)

    def griper(self, pop: int):
        """

        :param pop: кароче pop - попугаи от 1 до 255 на сколько раскрыт грипер
        """
        self.griper.gripper_action(pop)
