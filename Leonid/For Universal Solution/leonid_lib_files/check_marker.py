"""from leonid_lib"""
import cv2
import numpy
#importing libraries




def check_marker(img : numpy.ndarray, aruco_id : int = 17) -> bool:
    """Returns a Boolean value that indicates
    the presence of an ArUco Marker within the image.

    Keyword arguments:
    img -- the cv2 image where you need to find the ArUco Marker
    aruco_id -- ArUco Marker id (default 17)
    """
    aruco_detected = False
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    #setup

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, aruco_dict)
    if (res[1] is not None) and (len(res[1]) != 0):
         if len(numpy.where(res[1] == aruco_id)[0]) != 0:
             aruco_detected = True
    #mrker detection
             
    return aruco_detected
    #data Return
