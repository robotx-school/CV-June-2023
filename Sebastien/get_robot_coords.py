def get_robot_coords(coords):
    offset_x = 200
    offset_y = -145
    y_r = coords[0]
    x_r = coords[1]
    x_r, y_r = -y_r ,-x_r 
    x_r+=offset_x
    y_r+=offset_y
    coords[0] = x_r
    coords[1] = y_r
    return coords
    
