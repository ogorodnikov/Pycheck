from functools import reduce


def get_results(*functions):

    def inner_function(*args, **kwargs):

        if len(functions) > 1:
            return (inner(*args, **kwargs) for inner in map(get_results, functions))
        try:
            return functions[0](*args, **kwargs)
        except:
            return None

    return inner_function


def checkio(f, g):

    def h(*args, **kwargs):

        f_result, g_result = get_results(f, g)(*args, **kwargs)

        result = f_result if f_result is not None else g_result

        # alt_result = reduce(lambda a, b: a if a is not None else b,
        #                     get_results(f, g)(*args, **kwargs))

        status = ([None, 'both_error'][f_result is g_result is None] or
                  [None, 'same'][f_result == g_result] or
                  [None, 'f_error'][f_result is None] or
                  [None, 'g_error'][g_result is None] or 'different')

        output = result, status

        return output

    return h


if __name__ == '__main__':
    # (x+y)(x-y)/(x-y)
    assert checkio(lambda x, y: x + y,
                   lambda x, y: (x ** 2 - y ** 2) / (x - y)) \
               (1, 3) == (4, 'same'), "Function: x+y, first"
    assert checkio(lambda x, y: x + y,
                   lambda x, y: (x ** 2 - y ** 2) / (x - y)) \
               (1, 2) == (3, 'same'), "Function: x+y, second"
    assert checkio(lambda x, y: x + y,
                   lambda x, y: (x ** 2 - y ** 2) / (x - y)) \
               (1, 1.01) == (2.01, 'different'), "x+y, third"
    assert checkio(lambda x, y: x + y,
                   lambda x, y: (x ** 2 - y ** 2) / (x - y)) \
               (1, 1) == (2, 'g_error'), "x+y, fourth"

    # Remove odds from list
    f = lambda nums: [x for x in nums if ~x % 2]


    def g(nums):
        for i in range(len(nums)):
            if nums[i] % 2 == 1:
                nums.pop(i)
        return nums


    assert checkio(f, g)([2, 4, 6, 8]) == ([2, 4, 6, 8], 'same'), "evens, first"
    assert checkio(f, g)([2, 3, 4, 6, 8]) == ([2, 4, 6, 8], 'g_error'), "evens, second"

    # Fizz Buzz
    assert checkio(lambda n: ("Fizz " * (1 - n % 3) + "Buzz " * (1 - n % 5))[:-1] or str(n),
                   lambda n: ('Fizz' * (n % 3 == 0) + ' ' + 'Buzz' * (n % 5 == 0)).strip()) \
               (6) == ('Fizz', 'same'), "fizz buzz, first"
    assert checkio(lambda n: ("Fizz " * (1 - n % 3) + "Buzz " * (1 - n % 5))[:-1] or str(n),
                   lambda n: ('Fizz' * (n % 3 == 0) + ' ' + 'Buzz' * (n % 5 == 0)).strip()) \
               (30) == ('Fizz Buzz', 'same'), "fizz buzz, second"
    assert checkio(lambda n: ("Fizz " * (1 - n % 3) + "Buzz " * (1 - n % 5))[:-1] or str(n),
                   lambda n: ('Fizz' * (n % 3 == 0) + ' ' + 'Buzz' * (n % 5 == 0)).strip()) \
               (7) == ('7', 'different'), "fizz buzz, third"

    assert checkio(lambda n: ("Fizz " * (1 - n % 3) + "Buzz " * (1 - n % 5))[:-1] or str(n),
                   lambda n: ('Fizz' * (n % 3 == 0) + ' ' + 'Buzz' * (n % 5 == 0)).strip()) \
               (7) == ('7', 'different'), "fizz buzz, third"

    # Test 4

    f = lambda x: abs(x)


    def g(x):
        if x > 0:
            return x
        elif x < 0:
            return -x


    assert checkio(f, g)(0) == (0, 'g_error')


    # Test 3

    def f(hello="hello", world="world"):
        return hello + " " + world


    def g(hello, world="world"):
        return hello + " " + world


    assert checkio(f, g)('planet', hello='ahoi') == (None, 'both_error')
