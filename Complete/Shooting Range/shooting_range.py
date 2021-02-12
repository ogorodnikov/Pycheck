def determinant(column_a, column_b):
    ax, ay = column_a
    bx, by = column_b
    return ax * by - ay * bx


def get_line_coefficients(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b
    a = ay - by
    b = bx - ax
    c = determinant(point_a, point_b)
    return a, b, -c


def get_line_intersection(line1_coefficients, line2_coefficients):
    a1, b1, c1 = line1_coefficients
    a2, b2, c2 = line2_coefficients

    main_determinant = determinant((a1, b1), (a2, b2))
    determinant_x = determinant((c1, b1), (c2, b2))
    determinant_y = determinant((a1, c1), (a2, c2))
    print('Main determinant:', main_determinant)
    print('Determinant x:', determinant_x)
    print('Determinant y:', determinant_y)

    if main_determinant == 0:
        return None
    else:
        x = determinant_x / main_determinant
        y = determinant_y / main_determinant
        return x, y


def get_segment_center(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b
    dx = bx - ax
    dy = by - ay
    center_x = ax + dx / 2
    center_y = ay + dy / 2
    return center_x, center_y


def get_distance(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b
    dx = bx - ax
    dy = by - ay
    return (dx ** 2 + dy ** 2) ** 0.5


def shot(wall1, wall2, shot_point, later_point):
    print('Wall A:', wall1)
    print('Wall B:', wall2)
    print('Shot point:', shot_point)
    print('Later point:', later_point)

    wall_line_coefficients = get_line_coefficients(wall1, wall2)
    print('Wall line coefficients:', wall_line_coefficients)
    shot_line_coefficients = get_line_coefficients(shot_point, later_point)
    print('Shot line coefficients:', shot_line_coefficients)

    hit_coordinates = get_line_intersection(wall_line_coefficients, shot_line_coefficients)
    print('Hit coordinates:', hit_coordinates)

    if not hit_coordinates:
        print('No intersection')
        print()
        return -1

    wall_center = get_segment_center(wall1, wall2)
    print('Wall center:', wall_center)

    miss_distance = get_distance(wall_center, hit_coordinates)
    print('Miss distance:', miss_distance)

    wall_radius = get_distance(wall1, wall2) / 2
    print('Wall radius:', wall_radius)

    miss_fraction = miss_distance / wall_radius
    print('Miss fraction:', miss_fraction)

    if miss_fraction > 1:
        print('Missed')
        print()
        return -1

    is_direction_to_target = get_distance(shot_point, wall_center) > get_distance(later_point, wall_center)
    print('Is direction to target:', is_direction_to_target)

    if not is_direction_to_target:
        print('Other direction')
        return -1

    result = int(100 * (1 - miss_fraction) + 0.5)
    print('Result:', result)
    print()
    return result


if __name__ == '__main__':
    assert shot((2, 2), (5, 7), (11, 2), (8, 3)) == 100, "1st case"
    assert shot((2, 2), (5, 7), (11, 2), (7, 2)) == 0, "2nd case"
    assert shot((2, 2), (5, 7), (11, 2), (8, 4)) == 29, "3th case"
    assert shot((2, 2), (5, 7), (11, 2), (9, 5)) == -1, "4th case"
    assert shot((2, 2), (5, 7), (11, 2), (10.5, 3)) == -1, "4th case again"

    assert shot((2, 2), (5, 7), (8, 3), (11, 2)) == -1
    assert shot((10, 10), (10, 90), (50, 90), (50, 50)) == -1
    assert shot((10, 10), (10, 90), (70, 60), (50, 60)) == 75
