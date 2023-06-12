import urx, time
import numpy as np
import math3d as m3d


Home discharged_1 = [0.05931537911204936, -0.15447340760511827, 0.17628774555146742, 2.171678184767321, -2.2279843328133087, -0.17690443124182706]


Discharged_0 = [0.059310219869071666, -0.1544761812583753, 0.17629413083762654, 2.1716262818181113, -2.2280121942245676, -0.1769109124946434]


Cube = [0.024630305773663562, -0.4665363530546972, 0.17606659000022695, 2.1701663019594903, -2.2179679142674615, 0.024176359644519578]


Home = [0.0940783617936055, -0.0978777118391362, 0.40474269483904324, -2.1838818443602666, 2.231871391860771, 0.03631844607102951]






try:
    robot = urx.Robot('192.168.2.65')
    from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
    robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
    state = robot.getl()#
    print(state)#
except Exception as e:
    print('robot connection error',e)


def robot_go(coord,color):
    dest = {'orange':(-0.314,0.27),
            'green':(-0.169,0.3),
            'yellow':(-0.023,0.3)}
    x_min = -0.460
    x_max = -0.175
    y_min = -0.21
    y_max = 0.21
    time_delay = 0.1
    acc = 0.2
    speed = 0.2
    x = coord[0] / 1000
    y = coord[1] / 1000
    y-=0.02
    print(x, y)
    if x_min <= x <= x_max and y_min <= y <= y_max:
        print('go')

        
        if 0:
            state = robot.getl()
            print(state)
            robot.movel([-0.21, 0.25, 0.2, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            time.sleep(time_delay)
            robot.movel([x, y, 0.1, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            time.sleep(time_delay)
            robot.movel([x, y, 0.02, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            time.sleep(time_delay)
            robotiqgrip.gripper_action(150)

            robot.movel([dest[color][0], dest[color][1], 0.2, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            robot.movel([dest[color][0], dest[color][1], 0.12, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            robotiqgrip.gripper_action(0)
            robot.movel([dest[color][0], dest[color][1], 0.2, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)

            #home
            robot.movel([-0.21, 0.25, 0.2, 0.00, 3.14, 0.0], acc=acc, vel=speed, wait=True)
            time.sleep(time_delay)
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
