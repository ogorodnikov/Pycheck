from functools import lru_cache

MIN_DIGIT, MAX_DIGIT = 2, 10


@lru_cache(maxsize=None)
def deconstruct(number, level=0):
    xs = set()
    for divisor in range(MIN_DIGIT, MAX_DIGIT):
        quotient, remainder = divmod(number, divisor)
        # print('    ' * level + f'{number} = {divisor} * {quotient} + {remainder}')

        if not remainder:
            if MIN_DIGIT < quotient < MAX_DIGIT:
                divisor_deconstructs = deconstruct(divisor, level=level + 1)
                for divisor_deconstruct in divisor_deconstructs | {str(divisor)}:
                    xs.add(divisor_deconstruct + str(quotient))
                    # print('    ' * level + f'{number} -> \'{divisor_deconstruct} {quotient}\'')

            if MIN_DIGIT < quotient:
                quotient_deconstructs = deconstruct(quotient, level=level + 1)
                for quotient_deconstruct in quotient_deconstructs:
                    xs.add(str(divisor) + quotient_deconstruct)
                    # print('    ' * level + f'{number} -> \'{divisor} {quotient_deconstruct}\'')

    if not xs and MIN_DIGIT < number < MAX_DIGIT:
        xs = {str(number)}
    return xs


def checkio(number):
    print('Number:', number)

    xs = deconstruct(number)
    print('Xs:', xs)
    print('Deconstruct cache info :', deconstruct.cache_info())

    x_min = min(int(x) for x in xs or {0})
    print('X minimum:', x_min)
    print()
    return x_min


if __name__ == '__main__':
    assert checkio(134217728) == 888888888
    assert checkio(16777216) == 88888888
    assert checkio(2097152) == 8888888

    assert checkio(1024) == 2888
    assert checkio(6561) == 9999
    assert checkio(3645) == 5999

    assert checkio(20) == 45, "1st example"
    assert checkio(21) == 37, "2nd example"
    assert checkio(17) == 0, "3rd example"
    assert checkio(33) == 0, "4th example"
    assert checkio(3125) == 55555, "5th example"
    assert checkio(9973) == 0, "6th example"
