from math import pi


class Parameters:
    _shape = None

    def __init__(self, parameter):
        self._parameter = parameter

    def choose_figure(self, shape):
        self._shape = shape

    def perimeter(self):
        return self._shape.perimeter(self._parameter)

    def area(self):
        return self._shape.area(self._parameter)

class Circle:
    @staticmethod
    def perimeter(parameter):
        return 2 * pi * parameter

    @staticmethod
    def area(parameter):
        return round(pi * parameter ** 2, 2)


class Triangle:
    pass


class Square:
    pass


class Pentagon:
    pass


class Hexagon:
    pass


class Cube:
    pass


if __name__ == '__main__':

    figure = Parameters(10)

    figure.choose_figure(Circle())
    assert figure.area() == 314.16

    # figure.choose_figure(Triangle())
    # assert figure.perimeter() == 30
    #
    # figure.choose_figure(Square())
    # assert figure.area() == 100
    #
    # figure.choose_figure(Pentagon())
    # assert figure.perimeter() == 50
    #
    # figure.choose_figure(Hexagon())
    # assert figure.perimeter() == 60
    #
    # figure.choose_figure(Cube())
    # assert figure.volume() == 1000
