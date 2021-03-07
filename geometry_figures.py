from math import pi


class Parameters:
    _shape = None

    def __init__(self, parameter):
        self._parameter = parameter

    def choose_figure(self, shape):
        self._shape = shape

    def perimeter(self):
        return round(self._shape.perimeter(self._parameter), 2)

    def area(self):
        return round(self._shape.area(self._parameter), 2)

    def volume(self):
        if type(self._shape) is not Cube:
            return 0
        return round(self._shape.volume(self._parameter), 2)


class Circle:
    @staticmethod
    def perimeter(parameter):
        return 2 * pi * parameter

    @staticmethod
    def area(parameter):
        return pi * parameter ** 2


class Triangle:
    @staticmethod
    def perimeter(parameter):
        return 3 * parameter

    @staticmethod
    def area(parameter):
        return 3 ** 0.5 / 4 * parameter ** 2


class Square:
    @staticmethod
    def perimeter(parameter):
        return 4 * parameter

    @staticmethod
    def area(parameter):
        return parameter ** 2


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

    figure.choose_figure(Triangle())
    assert figure.perimeter() == 30

    figure.choose_figure(Square())
    assert figure.area() == 100

    # figure.choose_figure(Pentagon())
    # assert figure.perimeter() == 50
    #
    # figure.choose_figure(Hexagon())
    # assert figure.perimeter() == 60
    #
    # figure.choose_figure(Cube())
    # assert figure.volume() == 1000
