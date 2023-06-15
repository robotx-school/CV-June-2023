import cv2
import numpy as np

def find_robot(robot_zone_img):
    h_min = (0, 140, 173)
    h_max = (255, 255, 255)
    img_bin_r = cv2.inRange(robot_zone_img, h_min, h_max) 
    bitwiseNot_r = cv2.bitwise_not(img_bin_r) 
    summa = np.sum(bitwiseNot_r, axis=1) 
    dafk = np.where(summa > 10000) 
    
    if len(dafk[0]) > 1:
        return dafk[0][0], dafk[0][len(dafk[0]) - 1]
    else:
        return None, None
