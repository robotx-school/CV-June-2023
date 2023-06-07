import cv2
import numpy as np
dick = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
field = cv2.imread('field.jpg')
h_min=(0,140,173)
h_max=(255,255,255)

numba=0
save_h = np.array([])
use=0
