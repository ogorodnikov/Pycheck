from math import pi


class Parameters:
    _shape = None

    def __init__(self, parameter):
        self._parameter = parameter

    def choose_figure(self, shape):
        self._shape = shape

    @staticmethod
    def round_to_2_digits(function):
        def rounded_function():
            return round(function(), 2)

        return rounded_function

    def __getattr__(self, item):
        inner_attribute_getter = getattr(self._shape, item, lambda _: 0)

        @self.round_to_2_digits
        def redirected___getattr__():
            return inner_attribute_getter(self._parameter)

        return redirected___getattr__


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
    @staticmethod
    def perimeter(parameter):
        return 5 * parameter

    @staticmethod
    def area(parameter):
        return parameter ** 2 * (25 + 10 * 5 ** 0.5) ** 0.5 / 4


class Hexagon:
    @staticmethod
    def perimeter(parameter):
        return 6 * parameter

    @staticmethod
    def area(parameter):
        return parameter ** 2 * 3 * 3 ** 0.5 / 2


class Cube:
    @staticmethod
    def perimeter(parameter):
        return 12 * parameter

    @staticmethod
    def area(parameter):
        return parameter ** 2 * 6

    @staticmethod
    def volume(parameter):
        return parameter ** 3


if __name__ == '__main__':
    figure = Parameters(10)

    figure.choose_figure(Circle())
    assert figure.area() == 314.16

    figure.choose_figure(Triangle())
    assert figure.perimeter() == 30

    figure.choose_figure(Square())
    assert figure.area() == 100

    figure.choose_figure(Pentagon())
    assert figure.perimeter() == 50

    figure.choose_figure(Hexagon())
    assert figure.perimeter() == 60

    figure.choose_figure(Cube())
    assert figure.volume() == 1000

    figure = Parameters(100)
    figure.choose_figure(Circle())
    assert figure.volume() == 0
