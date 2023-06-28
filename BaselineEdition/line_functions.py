import cv2
import numpy as np

from find_aruco import find_aruco


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

def make_nice(coords):
    x1 = coords[1][1][0] - coords[1][0][0]
    y1 = coords[1][1][1] - coords[1][0][1]
    k1 = y1/x1
    b1 = coords[1][1][1] - k1 * coords[1][0][0]
    
    x2 = coords[0][1][0] - coords[0][0][0]
    y2 = coords[0][1][1] - coords[0][0][1]
    k2 = y2/x2
    b2 = coords[0][0][1] - k2 * coords[0][1][0]

    X = int((b2-b1)/(k1-k2))
    Y = int((X*k1)+b1)

    return [X,Y]



def line_funtik(frame,work_mod):
    if work_mod:
        _,__,pt0,pt1,pt2,pt3 = find_aruco(frame,1)[0]
        _,__,pt0_3,pt1_3,pt2_3,pt3_3 = find_aruco(frame,3)[0]
        C1 = make_nice([[pt0,pt1],[pt0_3,pt3_3]])
        C2 = make_nice([[pt0,pt3],[pt0_3,pt1_3]])
        pt0 = list(pt0)
        pt2_3 = list(pt2_3)
        #return [pt0,C1,pt2_3,C2]
        return [C1,pt0,C2,pt2_3]
    else:
        _,__,pt0,pt1,pt2,pt3 = find_aruco(frame,0)[0]
        _,__,pt0_3,pt1_3,pt2_3,pt3_3 = find_aruco(frame,2)[0] 
        C1 = make_nice([[pt0,pt1],[pt2_3,pt1_3]])
        C2 = make_nice([[pt0,pt3],[pt2_3,pt3_3]])
        pt1 = list(pt1)
        pt3_3 = list(pt3_3)
        #return [C1,pt1,C2,pt3_3]
        return [pt1,C1,pt3_3,C2]


