import cv2
import numpy as np
import math
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

def find_aruco_rotation(res_img):
    global dictionary
    c=[]
    gray = cv2.cvtColor(res_img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, dictionary)

    marker=17
    
    if res[1] is not None and marker in res[1]:
    
        index=np.where(res[1]==marker)[0][0]
        
        x1, y1 = int(res[0][index][0][0][0]), int(res[0][index][0][0][1])
        x2, y2 = int(res[0][index][0][1][0]), int(res[0][index][0][1][1])
        dx = x2 - x1
        dy = y2 - y1
        
           
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        dot_x = (res[0][index][0][0][0]+res[0][index][0][2][0])//2
        dot_y = (res[0][index][0][0][1]+res[0][index][0][2][1])//2
        
        return angle_deg, int(dot_x), int(dot_y)
    else:
        return None, None, None
