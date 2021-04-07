PRECISION = 5


def is_covered(room, sensors):
    width, height = room

    print('Room:', room)
    print('Sensors:', sensors)
    print('Width:', width)
    print('Height:', height)

    # elements_count = height * PRECISION
    #
    # numbers = [61 * i % elements_count for i in range(elements_count)]
    # print('Numbers:', numbers)
    # print('Len numbers :', len(numbers))
    #
    # quit()

    # is_all_covered = not any(all(abs(complex(y / PRECISION, x / PRECISION) - complex(sensor_y, sensor_x)) > sensor_radius
    #                          for sensor_x, sensor_y, sensor_radius in sensors)
    #                          for x in range(width * PRECISION)
    #                          for y in range(height * PRECISION))

    # is_all_covered = not any(
    #     all((((x / PRECISION - sensor_x) ** 2 + (y / PRECISION - sensor_y) ** 2) > sensor_radius ** 2)
    #         for sensor_x, sensor_y, sensor_radius in sensors)
    #     for y in range(height * PRECISION)
    #     for x in range(width * PRECISION))

    # is_all_covered = not any(
    #     all((((x - sensor_x * PRECISION) ** 2 + (y - sensor_y * PRECISION) ** 2) > (sensor_radius * PRECISION) ** 2)
    #         for sensor_x, sensor_y, sensor_radius in sensors)
    #     for y in range(height * PRECISION)
    #     for x in range(width * PRECISION))

    height_elements = height * PRECISION
    width_elements = width * PRECISION

    is_all_covered = not any(
        all((((x - sensor_x * PRECISION) ** 2 + (y - sensor_y * PRECISION) ** 2) > (sensor_radius * PRECISION) ** 2)
            for sensor_x, sensor_y, sensor_radius in sensors)
        for y in (61 * i % height_elements for i in range(height_elements))
        for x in (61 * i % width_elements for i in range(width_elements)))

    print('Is all covered:', is_all_covered)
    print()
    return is_all_covered

    # points = {complex(y / PRECISION, x / PRECISION) for x in range(width * PRECISION) for y in range(height * PRECISION)
    #           if all(abs(complex(y / PRECISION, x / PRECISION) - complex(sensor_y, sensor_x)) > sensor_radius
    #                  for sensor_x, sensor_y, sensor_radius in sensors)}
    #
    # print('Points:', points)
    #
    # max_point = max(points, key=abs)
    # min_point = min(points, key=abs)
    #
    # print('Max point:', max_point)
    # print('Min point:', min_point)
    #
    # quit()


if __name__ == '__main__':
    # assert is_covered([200, 150], [[100, 75, 130]]) == True
    # assert is_covered([200, 150], [[50, 75, 100], [150, 75, 100]]) == True
    # assert is_covered([200, 150], [[50, 75, 100], [150, 25, 50], [150, 125, 50]]) == False
    #
    # assert is_covered([200, 150], [[100, 75, 100], [0, 40, 60], [0, 110, 60], [200, 40, 60], [200, 110, 60]]) == True
    # assert is_covered([200, 150], [[100, 75, 100], [0, 40, 50], [0, 110, 50], [200, 40, 50], [200, 110, 50]]) == False
    # assert is_covered([200, 150], [[100, 75, 110], [105, 75, 110]]) == False
    # assert is_covered([200, 150], [[100, 75, 110], [105, 75, 20]]) == False
    # assert is_covered([3, 1], [[1, 0, 2], [2, 1, 2]]) == True
    # assert is_covered([30, 10], [[0, 10, 10], [10, 0, 10], [20, 10, 10], [30, 0, 10]]) == True
    # assert is_covered([30, 10], [[0, 10, 8], [10, 0, 7], [20, 10, 9], [30, 0, 10]]) == False

    assert is_covered([4000, 1000],
                      [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500], [2500, 200, 500], [2600, 800, 500],
                       [4000, 500, 1200], [1600, 500, 600]])
