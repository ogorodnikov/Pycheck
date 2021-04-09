from itertools import product
from fractions import Fraction
from random import randint

OPERATIONS = list('+-/*')
NUMBER_RANGE = (-100, 100)


def get_expressions(depth):

    if depth == 0:
        expressions = ["x-x", "x", "y"]

    else:
        sub_expressions = get_expressions(depth - 1)
        expression_parts = product(sub_expressions, OPERATIONS, sub_expressions)
        expressions = [''.join(parts).join('()') for parts in expression_parts]

    return expressions


def is_correct(expression, x, y):

    globals_dict = {"x": Fraction(x), "y": Fraction(y)}

    try:
        result = eval(expression, globals_dict)
        return [result.numerator, result.denominator]

    except ZeroDivisionError:
        return "ZeroDivisionError"


def checkio(steps, depth=0):

    while True:

        for expression in get_expressions(depth):

            if all(is_correct(expression, x, y) == result for x, y, result in steps):
                return expression, randint(*NUMBER_RANGE), randint(*NUMBER_RANGE)

        depth += 1


if __name__ == '__main__':

    def test_it(hidden_expression, solver):
        from fractions import Fraction
        from random import randint

        def check_is_right(guess, expression):
            for _ in range(10):
                result_guess = 0
                result_expr = 1
                for __ in range(100):
                    x, y = Fraction(randint(-100, 100)), Fraction(randint(-100, 100))
                    try:
                        result_expr = eval(expression)
                        result_guess = eval(guess)
                    except ZeroDivisionError:
                        continue
                    break
                if result_guess != result_expr:
                    return False
            return True

        input_data = []
        for step in range(50):
            user_guess, x_real, y_real = solver(input_data)
            x = Fraction(x_real)
            y = Fraction(y_real)
            try:
                result = eval(hidden_expression)
                output = [result.numerator, result.denominator]
            except ZeroDivisionError:
                output = "ZeroDivisionError"
            input_data.append([x_real, y_real, output])
            if check_is_right(user_guess, hidden_expression):
                return True
        else:
            return False

    assert test_it("x+y", checkio), "x+y"
    assert test_it("x*y", checkio), "x*y"
    assert test_it("x-y", checkio), "x-y"
    assert test_it("x/y", checkio), "x/y"
    assert test_it("y/x", checkio), "y/x"
    assert test_it("(x+y)*(x+y)", checkio)
