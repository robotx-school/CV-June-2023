def get_correct_coordinates(c,a):
    if c[0][0] is not None and c[0][1] is not None and c[0][2] is not None and c[0][3] is not None and c[0][4] is not None : 
        return [[c[0][0]+a, c[0][1]],
                c[1],
                [c[2][0]+a,c[2][1]],
                [c[3][0]+a,c[3][1]],
                [c[4][0]+a,c[4][1]],
                [c[5][0]+a,c[5][1]]]
    else:
        return [None]*5
