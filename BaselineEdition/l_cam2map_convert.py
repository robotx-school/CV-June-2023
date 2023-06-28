"""from leonid_lib"""
import cv2
import numpy
#importing libraries




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
