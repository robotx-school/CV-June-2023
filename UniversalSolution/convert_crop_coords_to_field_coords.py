def get_correct_coordinates(c,a):
    return list([c[0][0][0]+a, c[0][0][1]],
            c[0][1],
            [c[0][2][0]+a,c[0][2][1]],
            [c[0][3][0]+a,c[0][3][1]],
            [c[0][4][0]+a,c[0][4][1]],
            [c[0][5][0]+a,c[0][5][1]])
