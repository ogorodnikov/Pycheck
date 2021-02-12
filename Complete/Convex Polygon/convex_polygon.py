from itertools import starmap
from operator import mul


def checkio(data):
    ''' https://en.wikipedia.org/wiki/Shoelace_formula '''
    print('Polygon:', data)
    xs, ys = zip(*data + [data[0]])
    print('xs, ys:', xs, ys)
    polygon_area = abs(sum(starmap(mul, zip(xs, ys[1:]))) - sum(starmap(mul, zip(xs[1:], ys)))) / 2
    print('Polygon area:', polygon_area)
    print()
    return polygon_area


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=1):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    assert almost_equal(checkio([[1, 1], [9, 9], [9, 1]]), 32), "The half of the square"
    assert almost_equal(checkio([[4, 10], [7, 1], [1, 4]]), 22.5), "Triangle"
    assert almost_equal(checkio([[1, 2], [3, 8], [9, 8], [7, 1]]), 40), "Quadrilateral"
    assert almost_equal(checkio([[3, 3], [2, 7], [5, 9], [8, 7], [7, 3]]), 26), "Pentagon"
    assert almost_equal(checkio([[7, 2], [3, 2], [1, 5], [3, 9], [7, 9], [9, 6]]), 42), "Hexagon"
    assert almost_equal(checkio([[4, 1], [3, 4], [3, 7], [4, 8], [7, 9], [9, 6], [7, 1]]), 35.5), "Heptagon"
