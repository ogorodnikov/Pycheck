from cmath import phase, pi, e, tau
from itertools import starmap

PRECISION = 100


def get_convex_hull_points(points, center):
    """
    get convex hull points:
    - rotate input points by (2 * pi / PRECISION) radians at a time in a loop
    - find min_point with minimum distance to beginning of coordinates and add to min_point_indices
    - return points which indices are present in min_point_indices - which were min_point at least once
    """

    min_point_indices = set()

    for segment_index in range(PRECISION):

        new_points = []

        for point in points:

            moved_point = point - center
            rotated_point = moved_point * e ** (2j * pi * segment_index / PRECISION)
            moved_back_point = rotated_point + center

            new_points.append(moved_back_point)

        min_point = min(new_points, key=abs)
        min_point_index = new_points.index(min_point)

        min_point_indices.add(min_point_index)

    filtered_points = [point for index, point in enumerate(points) if index in min_point_indices]

    return filtered_points


def checkio(data):

    points = list(starmap(complex, data))

    center = sum(points) / len(points)

    convex_hull_points = get_convex_hull_points(points, center)

    starting_point = min(convex_hull_points, key=lambda c: (c.real, c.imag))

    starting_angle = -phase(starting_point - center) % tau

    # clockwise angles between (starting_point - center) vector and (point - center) vector
    angles = [((-phase(point - center) % tau - starting_angle) % tau, points.index(point))
              for point in convex_hull_points]

    sorted_angles = sorted(angles)

    output_indices = [record[1] for record in sorted_angles]

    return output_indices


if __name__ == '__main__':

    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    assert checkio(
        [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    ) == [1, 0, 6, 3, 5, 2], "Second example"

    assert checkio([[2, 6], [5, 5], [4, 4], [2, 2]]) == [3, 0, 1, 2]

    assert checkio([[1, 1], [1, 2], [1, 5], [5, 5], [5, 1]]) == [0, 1, 2, 3, 4]
