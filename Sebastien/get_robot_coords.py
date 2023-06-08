def get_robot_coords(coords_orange):
    offset_x = -143
    offset_y = 200
    robot_coords_orange = []
    for coord in coords_orange:
        print(coord)
        x_r = coord[0]+offset_x
        y_r = coord[1]+offset_y
        x_r, y_r = -y_r, x_r
        robot_coords_orange.append((x_r,y_r))
    
    return robot_coords_orange
test = get_robot_coords(((734,432),))  
print(test)
