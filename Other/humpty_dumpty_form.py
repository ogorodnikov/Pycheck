from math import pi, log, asin


def checkio(height, width):
    """
    https://en.wikipedia.org/wiki/Spheroid
    https://en.wikipedia.org/wiki/Sphere
    """

    print('Height:', height)
    print('Width:', width)

    a = width / 2
    c = height / 2

    volume = 4 * pi * a ** 2 * c / 3

    if height > width:
        print('Prolate spheroid')
        e = (1 - a ** 2 / c ** 2) ** 0.5
        surface = 2 * pi * a ** 2 * (1 + c / a / e * asin(e))
    elif height < width:
        print('Oblate spheroid')
        e = (1 - c ** 2 / a ** 2) ** 0.5
        surface = 2 * pi * a ** 2 + pi * c ** 2 / e * log((1 + e) / (1 - e))
    else:
        print('Sphere')
        surface = 4 * pi * a ** 2

    volume = round(volume, 2)
    surface = round(surface, 2)

    print('Volume:', volume)
    print('Surface:', surface)
    print()
    return [volume, surface]


if __name__ == '__main__':
    assert checkio(4, 2) == [8.38, 21.48], "Prolate spheroid"
    assert checkio(2, 2) == [4.19, 12.57], "Sphere"
    assert checkio(2, 4) == [16.76, 34.69], "Oblate spheroid"
