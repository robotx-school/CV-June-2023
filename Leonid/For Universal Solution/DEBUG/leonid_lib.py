"""Leonid's code for a comprehensive machine vision solution.
ROBOTX 2023

See functions check_marker(), l_cam2map_convert()

Use:
from leonid_lib import *"""
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
    

def l_cam2map_convert(coords : list,
                    k : list = [1.333, 1.56],
                    central_reflection : bool = True,
                    max_coords : list = [640, 480],
                    map_size : list = [600, 400]) -> list:
    """Returns coordinates in mm on the map using a linear
    function. If central reflection is enabled and x of
    the input coordinates is less than half of the maximum x,
    then the coefficient k of the linear function for x is
    multiplied by -1.

    Keyword arguments:
    coords -- cam coords
    k -- coefficients of a linear functions (default [1.333, 1.56])
    central_reflection -- using central reflection (default True)
    max_coords -- maximum camera coordinates (width and height) (default [640, 480])
    map_size -- map size (mm) (default [600, 400])"""
    return_coords = coords.copy()
    #setup
    
    if central_reflection:
        if coords[0] > max_coords[0]/2:
            return_coords[0] = round(coords[0]/(k[0]))
        else:
            return_coords[0] = (map_size[0]-20)//2 - ((map_size[0]-20)//2 + round(coords[0]/(k[0] * -1)))
    else:
        return_coords[0] = round(coords[0]/(k[0]))
    return_coords[1] = (map_size[1]-20) - round((max_coords[1] - coords[1])/(k[1]))
    #finding coordinates by y = kx

    return return_coords
    #data Return
    
        
if __name__ == "__main__":
    """Example (DEBUG) of using functions
    Must be used with accompanying files (see /DEBUG):
    cam - Leonid's personal code of the general type
    cam_correct - Stepan's code (typical)
    find_aruco - Ivan's code for finding ArUco Marker data"""
    print("DEBUG")
    from cam import get_image, cut_img, width, height
    import cam_correct
    from find_aruco import *
    #importing libraries
    

    while True:
        visual_layer = cv2.imread("field.png")
        frame = get_image()
        frame = cam_correct.undistort(frame)
        frame, lframe, rframe = cut_img(frame)
        #getting an image

        if check_marker(frame):
            #CHECKING FOR THE PRESENCE OF A ARUCO MARKER
            cam_coords = find_aruco(frame, 17)[0][0]    
            map_coords = l_cam2map_convert(cam_coords, max_coords = [width, height])
            #TRANSLATING COORDINATES FROM CAMERA TO MAP COORDINATES
            print(f"CAM: {cam_coords}, MAP: {map_coords}")
            frame = cv2.circle(frame, cam_coords, 10, (255, 0, 255), thickness = -1)
            visual_layer = cv2.circle(visual_layer, [map_coords[0] + 10, map_coords[1] + 10], 10, (0, 255, 255), thickness = -1)
        else:
            print("Marker not found!")
        
        cv2.imshow("Main", frame)
        cv2.imshow("Visual", visual_layer)
        #visualization
        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break


