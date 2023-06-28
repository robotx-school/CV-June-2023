"""from leonid_lib"""
import cv2
import numpy
#importing libraries




def e_cam2map_convert(img : numpy.ndarray,
                      aruco_id : int = 8,
                      ratio : list = [0.75, 0.75]) -> list:
    """Returns coordinates in mm on the map using a finding and
    corresponding coordinate transformation.

    Keyword arguments:
    img -- the cv2 image where you need to find coordinates
    aruco_id -- id of the ArUco Marker on the edge (default 8)
    ratio -- corresponding coordinate transformation (default [0.75, 0.75])
    """
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, aruco_dict)
    coords = []
    ox = -1
    oy = -1
    #setup

    if (res[1] is not None) and (len(res[1]) != 0):
        if len(numpy.where(res[1] == aruco_id)) != 0:
            coords = [[res[0][0][0][2][0], res[0][0][0][2][1]],
                           [res[0][0][0][3][0], res[0][0][0][3][1]]]
            
            ox = ((coords[0][0] + coords[1][0]) // 2) * ratio[0]
            oy = ((coords[0][1] + coords[1][1]) // 2) * ratio[1]
    #finding coordinates by down edge

    return [int(round(ox)), int(round(oy))]
    #data Return
