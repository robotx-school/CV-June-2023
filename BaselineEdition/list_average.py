"""For aggregate data from leonid_lib"""
def list_average(*args : list) -> list:
    """Returns a xy-list of the average
    values of all xy-lists.

    You can use:
    list_average(e_cam2map_convert(img, ...),
                 l_cam2map_convert(coords, ...))

    Positional arguments:
    *args - lists to get average data"""
    x, y = [], []
    for i in args:
        x.append(i[0])
        y.append(i[1])
        
    return([round(sum(x)/len(x)), round(sum(y)/len(y))])
