from math import e, pi

PRECISION = 1000


def is_covered(room, sensors):
    width, height = room

    for sensor in sensors:

        sensor_x, sensor_y, sensor_radius = sensor
        sensor_center = complex(sensor_y, sensor_x)

        locus = (sensor_center + sensor_radius * e ** (2j * pi * segment_index / PRECISION)
                 for segment_index in range(PRECISION + 1))

        locus_in_room = (point for point in locus
                         if height > point.real > 0
                         and width > point.imag > 0)

        # other_sensors = [other_sensor for other_sensor in sensors if sensor != other_sensor]

        other_sensors = set(map(tuple, sensors)) - {tuple(sensor)}

        is_locus_covered = all(any(abs(point - complex(other_y, other_x)) <= other_radius
                                   for other_x, other_y, other_radius in other_sensors)
                               for point in locus_in_room)

        if not is_locus_covered:
            return False

    return True


if __name__ == '__main__':

    assert is_covered([200, 150], [[100, 75, 130]]) == True
    assert is_covered([200, 150], [[50, 75, 100], [150, 75, 100]]) == True
    assert is_covered([200, 150], [[50, 75, 100], [150, 25, 50], [150, 125, 50]]) == False

    assert is_covered([200, 150], [[100, 75, 100], [0, 40, 60], [0, 110, 60], [200, 40, 60], [200, 110, 60]]) == True
    assert is_covered([200, 150], [[100, 75, 100], [0, 40, 50], [0, 110, 50], [200, 40, 50], [200, 110, 50]]) == False
    assert is_covered([200, 150], [[100, 75, 110], [105, 75, 110]]) == False
    assert is_covered([200, 150], [[100, 75, 110], [105, 75, 20]]) == False
    assert is_covered([3, 1], [[1, 0, 2], [2, 1, 2]]) == True
    assert is_covered([30, 10], [[0, 10, 10], [10, 0, 10], [20, 10, 10], [30, 0, 10]]) == True
    assert is_covered([30, 10], [[0, 10, 8], [10, 0, 7], [20, 10, 9], [30, 0, 10]]) == False

    assert is_covered([4000, 1000],
                      [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500], [2500, 200, 500], [2600, 800, 500],
                       [4000, 500, 1200], [1600, 500, 600]])

    assert is_covered([100, 100], [[50, 50, 65], [25, 25, 25], [25, 75, 25], [75, 25, 25], [75, 75, 25]]) == False
