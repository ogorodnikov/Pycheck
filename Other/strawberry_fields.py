from math import acos, pi


def strawberryfield(a, b, c, d):

    b, d = d, b

    # angle of cyclic quadrilateral:
    # https://en.wikipedia.org/wiki/Cyclic_quadrilateral#Angle_formulas

    alpha_cosine = (a ** 2 + b ** 2 - c ** 2 - d ** 2) / 2 / (a * b + c * d)
    alpha_radians = acos(alpha_cosine)
    alpha_degrees = alpha_radians / pi * 180
    rounded_alpha = round(alpha_degrees, 1)

    return rounded_alpha


if __name__ == '__main__':
    assert (strawberryfield(100, 100, 100, 100) == 90), "square"
    assert (strawberryfield(150, 100, 150, 100) == 90), "rectangle"
    assert (strawberryfield(150, 100, 50, 100) == 60), "trapezium"
    assert (strawberryfield(203, 123, 82, 117) == 60.8), "quadrilateral"
