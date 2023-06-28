"""For aggregate data from leonid_lib"""
import numpy
import cv2

def e_cam2map_cut(img : numpy.ndarray, image_split_coords : dict) -> list:
    """Returns a list of two cropped images for the two
    sides of the field. Used for e_cam2map_convert()

    Keyword arguments:
    img -- image to crop
    image_split_coords -- cropping parameters (from the config)"""
    width = img.shape[1]
    height = img.shape[0]

    limg = img.copy()
    rimg = img.copy()
    
    limg = cv2.rectangle(limg, (0, 0),(image_split_coords["robot_left_l_x"], height),(0, 0, 0), -1)
    limg = cv2.rectangle(limg, (image_split_coords["robot_left_r_x"], 0),(width, height),(0, 0, 0), -1)

    rimg = cv2.rectangle(rimg, (0, 0),(image_split_coords["robot_right_l_x"], height),(0, 0, 0), -1)
    rimg = cv2.rectangle(rimg, (image_split_coords["robot_right_r_x"], 0),(width, height),(0, 0, 0), -1) 
    
    return [limg, rimg]
