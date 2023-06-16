def fixed_proportion(coords : list, map_size : list = [600, 400], visual_size : list = [640, 480]) -> list:
    """Return coordinates in fixed proportion.

    Positional arguments:
    coords -- input coordinates
    map_size -- map size in mm (default: [600, 400])
    visual_size -- visualizer size in px (default: [640, 480])"""
    coords = [coords[0] + 50, coords[1] + 5]
    coords = [round(coords[0] * (visual_size[0] / map_size[0])),
              round(coords[1] * (visual_size[1] / map_size[1]))]
    return coords
