def checkio(steps):
    return ["x+y", 1, -1]


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
    # assert test_it("x*y", checkio), "x*y"
    # assert test_it("x-y", checkio), "x-y"
    # assert test_it("x/y", checkio), "x/y"
