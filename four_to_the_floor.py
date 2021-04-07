from math import e, pi, cos, sin

PRECISION = 1000

def is_covered(room, sensors):

    width, height = room

    for sensor in sensors:

        sensor_x, sensor_y, r = sensor
        sensor_center = complex(sensor_y, sensor_x)

        # locus = (sensor_center + r * e ** (2j * pi / PRECISION * segment) for segment in range(PRECISION + 1))
        locus = (sensor_center + r * (cos(pi / PRECISION * segment) + 1j * sin(pi / PRECISION * segment)) for segment in range(PRECISION + 1))

        locus_in_room = [point for point in locus if height >= point.real >= 0 and width >= point.imag >= 0]
        # print('Locus in room:', locus_in_room)

        # plot_complex_locus(locus_in_room)

        for point in locus_in_room:
            # print('Point:', point)

            is_in_others = False

            for other_sensor in sensors:
                if other_sensor == sensor:
                    continue
                # print('Other sensor:', other_sensor)

                other_x, other_y, other_r = other_sensor
                other_center = complex(other_y, other_x)

                if abs(point - other_center) <= other_r:
                    # print('---- Is in others')
                    # print('     Other center:', other_center)
                    # print('     Other r:', other_r)

                    is_in_others = True

            if not is_in_others:
                print('==== Not in others')
                return False

    print('All covered')
    return True

        # is_not_covered = any(abs(point - complex(sensor_y, sensor_x)) > sensor_radius
        #                      for point in locus_in_room
        #                      for sensor_x, sensor_y, sensor_radius in sensors)
        #
        # print('Is not covered:', is_not_covered)


    # print('Is all covered:', is_all_covered)
    # print()
    # return is_all_covered



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
