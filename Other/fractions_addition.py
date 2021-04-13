from fractions import Fraction


def add_fractions(fracts):

    fractions_sum = sum(Fraction(*fraction) for fraction in fracts)

    fraction_parts = divmod(fractions_sum, 1)

    fraction_output = ' and '.join(map(str, filter(None, fraction_parts)))

    try:
        fraction_output = int(fraction_output)
    except ValueError:
        pass

    return fraction_output

if __name__ == '__main__':

    assert add_fractions(((2, 3), (2, 3))) == "1 and 1/3"
    assert add_fractions(((1, 3), (1, 3))) == "2/3"
    assert add_fractions(((1, 3), (1, 3), (1, 3))) == 1
