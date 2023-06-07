def get_robot_coords(coords_orange, coords_green,coords_yellow):
    offset_x = -143
    offset_y = 200
    robot_coords_orange = []
    for coord in coords_orange:
        x_r = coord[0]+offset_x
        y_r = coord[1]+offset_y
        x_r, y_r = -y_r, x_r
        robot_coords_orange.append((x_r,y_r))
    robot_coords_green = []
    for coord in coords_green:
        x_r = coord[0] + offset_x
        y_r = coord[1] + offset_y
        x_r, y_r = -y_r, x_r
        robot_coords_green.append((x_r, y_r))
    robot_coords_yellow = []
    for coord in coords_yellow:
        x_r = coord[0] + offset_x
        y_r = coord[1] + offset_y
        x_r, y_r = -y_r, x_r
        robot_coords_yellow.append((x_r, y_r))
    return robot_coords_orange, robot_coords_green,robot_coords_yellow
    
