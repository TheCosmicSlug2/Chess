def color_clamp(color, add: int):
    """Force chaque composante R, G, B à rester entre 0 et 255."""
    r = min(max(0, color[0] + add), 255)
    g = min(max(0, color[1] + add), 255)
    b = min(max(0, color[2] + add), 255)
    return (r, g, b)

def get_dtuple(tuple1, tuple2):
    dpos = (tuple2[0] - tuple1[0], tuple2[1] - tuple1[1])
    return dpos

def add_tuples(tuple1, tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

def compare_tuples(tuple1, tuple2) -> int:
    """
    -1 : size1 is smaller
    0 : same size or one side is larger/the other is smaller
    1 : size1 is bigger
    """
    if tuple1[0] < tuple2[0] or tuple1[1] < tuple2[1]:
        return -1
    if tuple1[0] > tuple2[0] or tuple1[1] > tuple2[1]:
        return 1
    return 0