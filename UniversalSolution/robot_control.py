from config import *
import urx, time
import numpy as np
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

    def connect(self) -> bool:
        con = self.__check_connection__()
        if self.conn:
            return True
        if con != "sucses":
            self.conn = False
            raise Manipulator_Error(con)
        else:
            from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
            self.robot = urx.Robot(self.ip)
            self.griper = Robotiq_Two_Finger_Gripper(self.robot)
            self.conn = True
            return True

    def move_to(self, x: float, y: float, z: float, ang1: float, ang2: float, ang3: float, wait):
        """

        :param x: значение x куда приехать
        :param y: значение y куда приехать
        :param z: значение z куда приехать
        :param ang1: значение 1ого угла руки
        :param ang2: значение 2ого угла руки
        :param ang3: значение 3ого угла руки
        """
        if self.conn:
            self.robot.movel([x, y, z, ang1, ang2, ang3], acc=self.acc, vel=self.speed, wait=wait)
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


class Manipulator_Controler():
    def __init__(self, robot_left, robot_right):
        self.robot1 = robot_left
        self.robot2 = robot_right
        self.__check_connections__()

    def __check_connections__(self):
        self.robot1.connect()
        self.robot2.connect()

    def robot_control(self, data, right_cord, left_cord):
        self.robot1.move_to(left_cord["home"]["x"], left_cord["home"]["y"], left_cord["home"]["z"],
                            left_cord["home"]["a"],
                            left_cord["home"]["b"], left_cord["home"]["c"], True)

        self.robot2.move_to(right_cord["home"]["x"], right_cord["home"]["y"], right_cord["home"]["z"],
                            right_cord["home"]["a"],
                            right_cord["home"]["b"], right_cord["home"]["c"], True)

        self.robot1.griper(255)
        self.robot2.griper(255)

        if data["is_bat_left_robot"] != None and (data["is_bat_discharged_up"] or data["is_bat_discharged_down"]) and (data["is_bat_charged_up"] or data["is_bat_charged_down"]):
            self.robot1.move_to(data["is_bat_left_robot"]["x"], data["is_bat_left_robot"]["y"], 1,
                                data["is_bat_left_robot"]["ang"],
                                10, 10, True)

            if data["is_bat_charged_up"]:
                data["is_bat_charged_up"] = False
                self.robot2.move_to(left_cord["charged_up"]["x"], left_cord["charged_up"]["y"],
                                    left_cord["charged_up"]["z"],
                                    left_cord["charged_up"]["a"],
                                    left_cord["charged_up"]["b"], left_cord["charged_up"]["c"], True)
                self.robot2.griper(255)
            else:
                data["is_bat_charged_down"] = False
                self.robot2.move_to(left_cord["charged_down"]["x"], left_cord["charged_down"]["y"],
                                    left_cord["charged_down"]["z"],
                                    left_cord["charged_down"]["a"],
                                    left_cord["v"]["b"], left_cord["charged_down"]["c"], True)
                self.robot2.griper(255)

            data["is_bat_left_robot"] = None
            self.robot1.griper(1)
            if not data["is_bat_discharged_up"]:
                data["is_bat_discharged_up"] = True
                self.robot1.move_to(left_cord["discharged_up"]["x"], left_cord["discharged_up"]["y"],
                                    left_cord["discharged_up"]["z"],
                                    left_cord["discharged_up"]["a"],
                                    left_cord["discharged_up"]["b"], left_cord["discharged_up"]["c"], True)
                self.robot1.griper(255)
                self.robot2.move_to(data["is_bat_left_robot"]["x"], data["is_bat_left_robot"]["y"], 1,
                                    data["is_bat_left_robot"]["ang"],
                                    10, 10, True)
                self.robot2.griper(0)
            else:
                data["is_bat_discharged_down"] = True
                self.robot1.move_to(left_cord["discharged_down"]["x"], left_cord["discharged_down"]["y"],
                                    left_cord["discharged_down"]["z"],
                                    left_cord["discharged_down"]["a"],
                                    left_cord["discharged_down"]["b"], left_cord["discharged_down"]["c"], True)
                self.robot1.griper(255)
                self.robot2.move_to(data["is_bat_left_robot"]["x"], data["is_bat_left_robot"]["y"], 1,
                                    data["is_bat_left_robot"]["ang"],
                                    10, 10, True)
                self.robot2.griper(0)

        if data["is_bat_right_robot"] != None and (data["is_bat_discharged_up"] or data["is_bat_discharged_down"]) and (data["is_bat_charged_up"] or data["is_bat_charged_down"]):
            self.robot1.move_to(data["is_bat_right_robot"]["x"], data["is_bat_right_robot"]["y"], 1,
                                data["is_bat_right_robot"]["ang"],
                                10, 10, True)
            data["is_bat_right_robot"] = None
            self.robot1.griper(1)

            if data["is_bat_charged_up"]:
                data["is_bat_charged_up"] = False
                self.robot2.move_to(left_cord["charged_up"]["x"], left_cord["charged_up"]["y"],
                                    left_cord["charged_up"]["z"],
                                    left_cord["charged_up"]["a"],
                                    left_cord["charged_up"]["b"], left_cord["charged_up"]["c"], True)
                self.robot2.griper(255)
            else:
                data["is_bat_charged_down"] = False
                self.robot2.move_to(left_cord["charged_down"]["x"], left_cord["charged_down"]["y"],
                                    left_cord["charged_down"]["z"],
                                    left_cord["charged_down"]["a"],
                                    left_cord["v"]["b"], left_cord["charged_down"]["c"], True)
                self.robot2.griper(255)

            if not data["is_bat_discharged_up"]:
                data["is_bat_discharged_up"] = True
                self.robot1.move_to(left_cord["discharged_up"]["x"], left_cord["discharged_up"]["y"],
                                    left_cord["discharged_up"]["z"],
                                    left_cord["discharged_up"]["a"],
                                    left_cord["discharged_up"]["b"], left_cord["discharged_up"]["c"], True)
                self.robot1.griper(255)
                self.robot2.move_to(data["is_bat_right_robot"]["x"], data["is_bat_right_robot"]["y"], 1,
                                    data["is_bat_right_robot"]["ang"],
                                    10, 10, True)
                self.robot2.griper(0)
            else:
                data["is_bat_discharged_down"] = True
                self.robot1.move_to(left_cord["discharged_down"]["x"], left_cord["discharged_down"]["y"],
                                    left_cord["discharged_down"]["z"],
                                    left_cord["discharged_down"]["a"],
                                    left_cord["discharged_down"]["b"], left_cord["discharged_down"]["c"], True)
                self.robot1.griper(255)
                self.robot2.move_to(data["is_bat_right_robot"]["x"], data["is_bat_right_robot"]["y"], 1,
                                    data["is_bat_right_robot"]["ang"],
                                    10, 10, True)
                self.robot2.griper(0)


if __name__ == "__main__":
    robot = Manipulator(ROBOT_IP, ROBOT_ACEL, ROBOT_SPEED)
    d = Manipulator_Controler(robot, robot)
    data = [
        {"is_bat_right_robot": None},
        {"is_bat_left_robot": {"x":10,"y":10,"ang":10}},
        {"is_bat_charged_down": True},
        {"is_bat_discharged_down": False},
        {"is_bat_charged_up": False},
        {"is_bat_discharged_up": True}
    ]
    d.robot_control(data, robotright, robotleft)
