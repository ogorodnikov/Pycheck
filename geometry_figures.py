class Parameters:
    pass


class Circle:
    pass


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
