from math import e, pi, exp

from matplotlib import pyplot, patches

def is_covered(room, sensors):

    def plot_complex_locus(locus):

        locus_y = [point.real for point in locus]
        locus_x = [point.imag for point in locus]

        figure, axes = pyplot.subplots()

        room_patch = patches.Rectangle((0, 0), width, height, linewidth=2, edgecolor='k', facecolor='none')
        axes.add_patch(room_patch)

        axes.plot(locus_x, locus_y)
        axes.set(xlim=(width * -0.5, width * 1.5), ylim=(height * -0.5, height * 1.5))

        axes.grid()

        pyplot.show()


    width, height = room

    print('Room:', room)
    print('Sensors:', sensors)
    print('Width:', width)
    print('Height:', height)

    segment_count = 100

    for sensor in sensors:
        print('Sensor:', sensor)

        x0, y0, r = sensor

        locus = [complex(y0, x0) + r * e ** (2j * pi / segment_count * segment) for segment in range(segment_count + 1)]
        # print('Locus:', locus)

        locus_in_room = [point for point in locus if height >= point.real >= 0 and width >= point.imag >= 0]
        print('Locus in room:', locus_in_room)

        # plot_complex_locus(locus_in_room)

        for point in locus_in_room:
            print('Point:', point)

            is_in_others = False

            for other_sensor in sensors:
                if other_sensor == sensor:
                    continue
                print('Other sensor:', other_sensor)

                other_x, other_y, other_r = other_sensor
                other_center = complex(other_y, other_x)

                if abs(point - other_center) <= other_r:
                    print('---- Is in others')
                    print('     Other center:', other_center)
                    print('     Other r:', other_r)

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
