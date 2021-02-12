def get_linear_coefficients(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b
    dx = bx - ax
    dy = by - ay
    if dx == 0:
        slope = float('inf')
    else:
        slope = dy / dx
    y_intercept = ay - ax * slope
    return slope, y_intercept


def get_line_intersection(slope_a, intercept_a, slope_b, intercept_b):
    x = (intercept_a - intercept_b) / (slope_b - slope_a)
    print('X 1:', intercept_a - intercept_b)
    print('X 2:', slope_b - slope_a)
    print('X:', x)
    y = x * slope_a + intercept_a
    print('Y:', y)
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

    wall_slope, wall_intercept = get_linear_coefficients(wall1, wall2)
    print('Wall slope:', wall_slope)
    print('Wall intercept:', wall_intercept)

    shot_slope, shot_intercept = get_linear_coefficients(shot_point, later_point)
    print('Shot slope:', shot_slope)
    print('Shot intercept:', shot_intercept)

    hit_coordinates = get_line_intersection(wall_slope, wall_intercept, shot_slope, shot_intercept)
    print('Hit coordinates:', hit_coordinates)

    wall_center = get_segment_center(wall1, wall2)
    print('Wall center:', wall_center)

    miss_distance = get_distance(wall_center, hit_coordinates)
    print('Miss distance:', miss_distance)

    wall_radius = get_distance(wall1, wall2) / 2
    print('Wall radius:', wall_radius)

    miss_fraction = miss_distance / wall_radius
    print('Miss fraction:', miss_fraction)

    is_direction_to_target = get_distance(shot_point, wall_center) > get_distance(later_point, wall_center)
    print('Is direction to target:', is_direction_to_target)

    if miss_fraction > 1 or miss_fraction != miss_fraction or not is_direction_to_target:
        result = -1
    else:
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
