def get_robot_coords(coords):
    print(coords[0])
    #offset_x = -205
    #offset_y = -75
    offset_x = 205
    offset_y = 75
    robot_coords = []
    x_r = coords[0]+offset_x
    y_r = coords[1]+offset_y
    x_r, y_r = y_r, -x_r
    robot_coords.append((x_r, y_r))
    return robot_coords

test = get_robot_coords([333, 282])  

print(test)
