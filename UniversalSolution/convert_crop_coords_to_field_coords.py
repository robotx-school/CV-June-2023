
def get_correct_coordinates(c,a):
    if c[0] is not None and c[1] is not None and c[2] is not None and c[3] is not None and c[4] is not None and c[5] is not None: 
        return [[c[0][0]+a, c[0][1]],
                c[1],
                [c[2][0]+a,c[2][1]],
                [c[3][0]+a,c[3][1]],
                [c[4][0]+a,c[4][1]],
                [c[5][0]+a,c[5][1]]]
    else:
        return [None]*5


# PUT vanyas LIST and image_split_coords['robot_left_l_x'] for example or any other element in our dictionary
'''
image_split_coords = {'robot_left_l_x': 90,
                      'robot_left_r_x':320,
                      'robot_right_l_x':320,
                      'robot_right_r_x':550}
c = [None]*5#[[0,0],90,[30,30],[30,40],[40,30],[40,40]]
print(image_split_coords['robot_left_l_x'])
test=get_correct_coordinates(c,image_split_coords['robot_left_l_x'])
print(test)

'''
