import cv2
import numpy as np

def find_robot(robot_zone_img):
    h_min = (0, 108, 170)
    h_max = (15, 255, 255)
    img_bin_r = cv2.inRange(robot_zone_img, h_min, h_max) 
    kernel = np.ones((5, 5), 'uint8')
    thresh = cv2.erode(img_bin_r, kernel, iterations=4)
    img_bin_r = cv2.dilate(thresh, kernel, iterations=3)
    
    bitwiseNot_r = cv2.bitwise_not(img_bin_r)
    summa = np.sum(bitwiseNot_r, axis=1)
    dafk = np.where(summa > 10000) 
    
    if len(dafk[0]) > 1:
        return dafk[0][0], dafk[0][len(dafk[0]) - 1]
    else:
        return None, None
