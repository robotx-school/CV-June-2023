from config import *
import urx, time
import math3d as m3d


class Manipulator_Error(Exception):
    def __init__(self, error):
        self.message = error

    def __str__(self):
        return 'We try to connect, but: {0}'.format(self.message)

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
                return "GetlERROR"

        except Exception as e:
            ret = e
            return ret

    def connect(self) -> str:
        con = self.__check_connection__()
        if con != "sucses":
            self.conn = False
            raise Manipulator_Error(con)
        else:
            from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
            self.robot = urx.Robot(self.ip)
            self.griper = Robotiq_Two_Finger_Gripper(self.robot)
            self.conn = True

    def move(self, x: float, y: float, z: float, ang1: float, ang2: float, ang3: float):
        """

        :param x: значение x куда приехать
        :param y: значение y куда приехать
        :param z: значение z куда приехать
        :param ang1: значение 1ого угла руки
        :param ang2: значение 2ого угла руки
        :param ang3: значение 3ого угла руки
        """
        if self.conn:
            self.robot.movel([x, y, z, ang1, ang2, ang3], acc=self.acc, vel=self.speed, wait=True)
        else:
            raise Manipulator_Error("we don`t try to connect")

    def griper(self, pop: int):
        """

        :param pop: кароче pop - попугаи от 1 до 255 на сколько раскрыт грипер
        """
        if self.conn:
            self.griper.gripper_action(pop)
        else:
            raise Manipulator_Error("we don`t try to connect")

if __name__ == "__main__":
    robot = Manipulator(ROBOT_IP, ROBOT_ACEL, ROBOT_SPEED)
    robot.connect()
    #robot.move
