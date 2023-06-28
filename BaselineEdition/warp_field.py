import cv2
import numpy as np
from line_functions import line_funtik
import math
def warp_field(img,aruco_dict):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray,aruco_dict)
    coords = [0,0,0,0]
    
    with open("123.txt","r",encoding = "utf-8") as file:
        coord = eval(file.readline())
    
    if res[1] is not None and (0 in res[1] and 1 in res[1] and 2 in res[1] and 3 in res[1]):
        for i in range(4):
            marker = i
            index = np.where(res[1] == marker)[0][0]
            pt0 = res[0][index][0][marker].astype(np.int16)
            coords[i] = list(pt0)
        with open("123.txt","w",encoding = "utf-8") as file:
            file.write(str(coords))




    
    elif res[1] is not None and (0 in res[1] and 2 in res[1]):
        index = np.where(res[1] == 0)[0][0]
        pt0 = res[0][index][0][0].astype(np.int16)
        print(math.fabs(coord[0][1] - pt0[1]))
        if math.fabs(coord[0][0] - pt0[0])>=5 and math.fabs(coord[0][1] - pt0[1])>=5:
            coords = line_funtik(img,0)

        else:
            coords = coord
        



        
    elif res[1] is not None and (1 in res[1] and 3 in res[1]):
        index = np.where(res[1] == 1)[0][0]
        pt0 = res[0][index][0][1].astype(np.int16)
        print(math.fabs(coord[0][1] - pt0[1]))
        if math.fabs(coord[0][0] - pt0[0])>=5 and math.fabs(coord[0][1] - pt0[1])>=5:
            coords = line_funtik(img,1)
        else:
            coords = coord


    else:
        with open("123.txt","r",encoding = "utf-8") as file:
            coords = eval(file.readline())

    
    


    print(coords)
    height, weight, _ = img.shape
    input_pt = np.array(coords)
    output_pt = np.array([[0,0],[weight,0],[weight,height],[0,height]])
    h,_ = cv2.findHomography(input_pt, output_pt)
    res_img = cv2.warpPerspective(img,h,(weight,height))
    return res_img
