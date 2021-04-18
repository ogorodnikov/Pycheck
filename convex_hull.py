PRECISION = 10

from itertools import starmap


def checkio(data):
    print('Data:', data)

    complex_points = list(starmap(complex, data))
    print('Complex points:', complex_points)

    min_x, max_x, min_y, max_y = (operation(map(part, complex_points))
                                  for part in (lambda c: c.real, lambda c: c.imag)
                                  for operation in (min, max))

    print('Min x:', min_x)
    print('Max x:', max_x)
    print('Min y:', min_y)
    print('Max y:', max_y)

    center = complex(min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2)
    print('Center:', center)

    center = sum(complex_points) / len(complex_points)
    print('Center:', center)

    quit()

    for step in range(PRECISION):
        print('Step:', step)

        for point in complex_points:
            print('    Point:', point)

    quit()

    return [0, 1, 2]


if __name__ == '__main__':
    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    # assert checkio(
    #     [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    # ) == [1, 0, 6, 3, 5, 2], "Second example"
