import cv2
import numpy as np

def find_robot_battery(robot_zone_img,num,dictionary):
    gray2 = cv2.cvtColor(robot_zone_img,cv2.COLOR_BGR2GRAY)
    res2 = cv2.aruco.detectMarkers(gray2,dictionary)
    output = []
    qqq = np.where(res2[1] == num)[0]
    try:
        for i in range(len(np.where(res2[1] == num)[0])):
            index = np.where(res2[1] == num)[0][i]
            pt0= res2[0][index][0][0].astype(np.int16)
            pt1 = res2[0][index][0][1].astype(np.int16)
            pt2 = res2[0][index][0][2].astype(np.int16)
            pt3 = res2[0][index][0][3].astype(np.int16)
            center = [(pt0[0] + pt2[0])//2,(pt0[1] + pt2[1])//2]
            tmp_angle = 0
            kat_0 = pt1[0] - pt0[0]
            kat_1 = pt1[1] - pt0[1]
            tg = kat_1 / kat_0
            tmp_angle = math.atan(tg)
            tmp_angle = math.degrees(tmp_angle)
            tmp_angle = math.fabs(tmp_angle)
            tmp_angle = int(tmp_angle)
            output.append([center,tmp_angle,pt0,pt1,pt2,pt3])
        return output
    except:
        for i in qqq:
            output.append([None,None,None,None,None,None])
        return output
    
