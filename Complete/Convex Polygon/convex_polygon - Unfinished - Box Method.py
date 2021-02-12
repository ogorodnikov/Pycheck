from itertools import tee, chain


def get_cycled_pairs(iterable):
    a, b = tee(iterable)
    b = chain(b, [next(b, None)])
    return zip(a, b)


def get_inner_point(convex_polygon_vertices):
    xs, ys = zip(*convex_polygon_vertices)
    max_x, min_x = max(xs), min(xs)
    max_y, min_y = max(ys), min(ys)
    inner_point = min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2
    return inner_point


def right_triangle_area(point_p, point_q):
    (px, py) = point_p
    (qx, qy) = point_q
    return abs(px - qx) * abs(py - qy) / 2


def get_triangle_area(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    square_dx = max(ax, bx, cx) - min(ax, bx, cx)
    square_dy = max(ay, by, cy) - min(ay, by, cy)
    print('    Square dx:', square_dx)
    print('    Square dy:', square_dy)
    area = square_dx * square_dy
    print('    Square area:', area)
    for point_p, point_q in get_cycled_pairs((a, b, c)):
        print('        Point p:', point_p)
        print('        Point q:', point_q)
        (px, py) = point_p
        (qx, qy) = point_q
        dx = abs(px - qx)
        dy = abs(py - qy)
        print('        dx:', dx)
        print('        dy:', dy)
        right_triangle_area = dx * dy / 2
        print('        - Right triangle area:', right_triangle_area)
        area -= right_triangle_area
        additional_triangle_area = (min(dx, (square_dx - dx))) * (min(dy, (square_dy - dy))) / 2
        print('        - Additional triangle area:', additional_triangle_area)
        area -= additional_triangle_area
        print('        = Area:', area)
    print('    Complete area:', area)
    return area


def checkio(data):
    print('Polygon:', data)
    inner_point = get_inner_point(data)
    print('Inner point:', inner_point)

    print('Adding sub-triangles')
    polygon_area = 0
    for a, b in get_cycled_pairs(data):
        print('    Vertices:', (a, b, inner_point))
        triangle_area = get_triangle_area(a, b, inner_point)
        print('    Triangle area:', triangle_area)
        polygon_area += triangle_area

    print('Polygon area:', polygon_area)
    print()
    return polygon_area


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=1):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    # assert almost_equal(checkio([[1, 1], [9, 9], [9, 1]]), 32), "The half of the square"
    assert almost_equal(checkio([[4, 10], [7, 1], [1, 4]]), 22.5), "Triangle"
    # assert almost_equal(checkio([[1, 2], [3, 8], [9, 8], [7, 1]]), 40), "Quadrilateral"
    # assert almost_equal(checkio([[3, 3], [2, 7], [5, 9], [8, 7], [7, 3]]), 26), "Pentagon"
    # assert almost_equal(checkio([[7, 2], [3, 2], [1, 5], [3, 9], [7, 9], [9, 6]]), 42), "Hexagon"
    # assert almost_equal(checkio([[4, 1], [3, 4], [3, 7], [4, 8], [7, 9], [9, 6], [7, 1]]), 35.5), "Heptagon"
