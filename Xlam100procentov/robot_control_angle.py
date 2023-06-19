import urx, time
import numpy as np
import math3d as m3d
import math
import numpy as np
try:
    robot = urx.Robot('192.168.2.65')
    from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
    robotiqgrip = Robotiq_Two_Finger_Gripper(robot)
except Exception as e:
    print('robot connection error',e)

state = robot.getl()
print(state)




def angle_gripper(angle):
    roll = 0
    pitch = 3.14
    yaw = np.deg2rad(angle)

    print ("roll = ", roll)
    print ("pitch = ", pitch)
    print ("yaw = ", yaw)
    print ("")

    yawMatrix = np.matrix([
    [math.cos(yaw), -math.sin(yaw), 0],
    [math.sin(yaw), math.cos(yaw), 0],
    [0, 0, 1]
    ])

    pitchMatrix = np.matrix([
    [math.cos(pitch), 0, math.sin(pitch)],
    [0, 1, 0],
    [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    rollMatrix = np.matrix([
    [1, 0, 0],
    [0, math.cos(roll), -math.sin(roll)],
    [0, math.sin(roll), math.cos(roll)]
    ])

    R = yawMatrix * pitchMatrix * rollMatrix

    theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
    multi = 1 / (2 * math.sin(theta))

    rx = multi * (R[2, 1] - R[1, 2]) * theta
    ry = multi * (R[0, 2] - R[2, 0]) * theta
    rz = multi * (R[1, 0] - R[0, 1]) * theta
    rz = 0
    
    return rx, ry, rz


rx,ry,rz = angle_gripper(90)
print(rx,ry,rz)
#robot.movel([0.021, -0.39, 0.18, rx, ry, rz] , 0.1 , 0.2, wait = True)



