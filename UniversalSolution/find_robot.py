import cv2
import numpy as np

def find_robot(robot_zone_img):
    h_min = (20, 140, 173)# red minimum value
    h_max = (255, 255, 255)# red maximum value
    img_bin_r = cv2.inRange(robot_zone_img, h_min, h_max) # cropped black and white version
    bitwiseNot_r = cv2.bitwise_not(img_bin_r) # invert img_bin
    summa = np.sum(bitwiseNot_r, axis=1) # creates an array of sum values
    dafk = np.where(summa>10000) # coordinates of values over 10000
    
    if len(dafk[0])>1: # if at least 2 red pixels exist
        return dafk[0][0], dafk[0][len(dafk[0])-1]
    else:
        return None, None
