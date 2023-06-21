import numpy as np
import cv2

def fit_all_img_together(undistort,warp,visualize):
    undistort = cv2.resize(undistort,(undistort.shape[1]//2,undistort.shape[0]//2))
    warp = cv2.resize(warp,(warp.shape[1]//2,warp.shape[0]//2))
    undistort_and_warp = cv2.vconcat([undistort,warp])
    visualize = cv2.hconcat([visualize,undistort_and_warp])
    return visualize
