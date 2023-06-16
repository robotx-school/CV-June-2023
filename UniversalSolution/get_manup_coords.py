def get_l_manup_cords(x_y):
    l_manup_coords = []
    offset_x = -80
    offset_y = 200
    x, y = x_y[0], x_y[1]
    x_r, y_r = -y + offset_y, -x + offset_x
    l_manup_coords.append(x_r)
    l_manup_coords.append(y_r)
    return l_manup_coords

def get_r_manup_cords(x_y):
    r_manup_coords = []
    offset_x = 80
    offset_y = 200
    x, y = x_y[0], x_y[1]
    x_r, y_r = y + offset_y, x + offset_x
    r_manup_coords.append(x_r)
    r_manup_coords.append(y_r)
    return r_manup_coords
