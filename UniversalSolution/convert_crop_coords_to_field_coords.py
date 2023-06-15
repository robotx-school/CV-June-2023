
def robot_right_top(c):
    
    return [[c[0][0]+550, c[0][1]],c[1],c[2],c[3],c[4],c[5]]

def robot_right_bottom(c):
    return [[c[0][0]+550, c[0][1]+240],c[1],c[2],c[3],c[4],c[5]]

def robot_left_top(c):
    return [[c[0][0], c[0][1]],c[1],c[2],c[3],c[4],c[5]]

def robot_left_bottom(c):
    return [[c[0][0], c[0][1]+240],c[1],c[2],c[3],c[4],c[5]]

def right_robot_battery(c):
    return [[c[0][0]+90, c[0][1]],c[1],c[2],c[3],c[4],c[5]]

def left_robot_battery(c):
    return [[c[0][0]+320, c[0][1]],c[1],c[2],c[3],c[4],c[5]]
