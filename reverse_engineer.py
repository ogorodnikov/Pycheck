denominator = '1'
numerator = '1'

def checkio(steps):
    print('Steps:', steps)

    global denominator

    if len(steps) == 0:
        return ['1', 0, 2]

    if len(steps) == 1:

        if steps[-1][2] == 'ZeroDivisionError':
            denominator = 'x'
        else:
            return ['1', 2, 0]

    if len(steps) == 2:

        if steps[-1][2] == 'ZeroDivisionError':
            denominator = 'y'
        else:
            pass

        print('Denominator:', denominator)
        quit()


    return [f'{numerator}/{denominator}', 5, 5]


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


    # assert test_it("x+y", checkio), "x+y"
    # assert test_it("x*y", checkio), "x*y"
    # assert test_it("x-y", checkio), "x-y"
    # assert test_it("x/y", checkio), "x/y"
    # assert test_it("y/x", checkio), "y/x"
