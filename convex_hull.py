from math import pi, e

PRECISION = 100

from itertools import starmap


def get_center(points):

    # return sum(points) / len(points)

    min_x, max_x, min_y, max_y = (operation(map(part, points))
                                  for part in (lambda c: c.real, lambda c: c.imag)
                                  for operation in (min, max))

    return complex(min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2)


def checkio(data):

    # data = [[1, 2], [2, 1], [2, 3], [3, 2]]
    # data = [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9], [4, 4]]

    print('Data:', data)

    complex_points = list(starmap(complex, data))
    print('Complex points:', complex_points)

    center = get_center(complex_points)
    print('Center:', center)



    min_point_indices = []

    for segment_index in range(PRECISION):
        print('Segment index:', segment_index)
        
        new_points = []

        for point in complex_points:
            print('    Point:', point)

            moved_point = point - center
            print('        Moved point:', moved_point)

            rotated_point = moved_point * e ** (2j * pi * segment_index / PRECISION)
            print('        Rotated point:', rotated_point)
            
            new_point = rotated_point + center
            print('        New point:', new_point)
            
            new_points.append(new_point)

        print('New points:', new_points)
        
        min_point = min(new_points, key=abs)
        print('Min point:', min_point)
        
        min_point_index = new_points.index(min_point)
        print('Min point index:', min_point_index)

        min_point_indices.append(min_point_index)

    print()
    print('Min point indices:', min_point_indices)

    filtered_points = [point for index, point in enumerate(complex_points) if index in min_point_indices]
    print('Filtered points:', filtered_points)

    min_point = min(filtered_points, key=lambda c: (c.real, c.imag))
    print('Min point:', min_point)

    min_index = filtered_points.index(min_point)
    print('Min index:', min_index)

    shifted_points = filtered_points[min_index:] + filtered_points[:min_index]
    print('Shifted points:', shifted_points)

    shifted_indices = [filtered_points.index(point) for point in shifted_points]
    print('Shifted indices:', shifted_indices)
    print()
    return shifted_indices


if __name__ == '__main__':

    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    # assert checkio(
    #     [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    # ) == [1, 0, 6, 3, 5, 2], "Second example"
