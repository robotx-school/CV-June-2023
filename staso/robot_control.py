import urx, time
import numpy as np
import math3d as m3d
try:
    robot = urx.Robot('192.168.137.60')
    from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
    robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
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
