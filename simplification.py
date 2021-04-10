import re
from collections import defaultdict


def parse_polynomial(polynomial_string):
    """ parse polynomial_string to dictionary {degree: coefficient} """

    terms = re.findall(r'(([+-]?\d?).+?)(?=[+-]|$)', polynomial_string)
    print('Terms:', terms)

    polynomial = defaultdict(int)

    for term, coefficient in terms:

        if coefficient == '':
            coefficient = '+1'
        else:
            if coefficient[0] not in '+-':
                coefficient = '+' + coefficient
            if coefficient[-1] in '+-':
                coefficient = coefficient + '1'

        degree = term.count('x')

        # print('Term:', term)
        # print('    Coefficient:', coefficient)
        # print('    Degree:', degree)

        polynomial[degree] += int(coefficient)

    # print('Polynomial:', polynomial)

    return polynomial


def reduce_polynomial(expression):
    print('Reduce expression:', expression)

    sub_expressions = re.findall(r'(\(.?\))', expression)
    print('Sub expressions:', sub_expressions)

    quit()

    return parse_polynomial(expr)


def polynomial_to_string(polynomial):
    print('Polynomial:', polynomial)

    polynomial_string = ''

    for degree, coefficient in polynomial.items():

        if coefficient == 1 and degree == max(degree for degree, coefficient in polynomial.items()):
            coefficient_string = ''

        elif coefficient in (1, -1) and degree > 0:
            coefficient_string = f'{coefficient:+d}'[:-1]

        else:
            coefficient_string = f'{coefficient:+d}'

        if degree == 0:
            degree_string = ''
        elif degree == 1:
            degree_string = f'x'
        else:
            degree_string = f'x**{degree}'

        # print('Coefficient:', coefficient)
        # print('Degree:', degree)
        # print('    Coefficient string:', coefficient_string)
        # print('    Degree string:', degree_string)
        # print()

        if coefficient_string == '-':
            term_symbol = ''
        else:
            term_symbol = '*'

        term_string = term_symbol.join(filter(None, (coefficient_string, degree_string)))

        polynomial_string += term_string

    print('Polynomial string:', polynomial_string)
    return polynomial_string


def simplify(expr):
    print('Expr:', expr)

    resulting_polynomial = reduce_polynomial(expr)

    resulting_polynomial_string = polynomial_to_string(resulting_polynomial)

    print('Resulting polynomial string:', resulting_polynomial_string)
    print()
    return resulting_polynomial_string


def encode(message):
    def write_transparently(_, token):
        return token

    def write_ascii_code(_, token):
        return f'{ord(token):<07b}'

    scanner = re.Scanner([(r'\d|[^\w\s]', write_transparently),
                          (r'.', write_ascii_code)])

    tokens, unrecognised = scanner.scan(message)

    return ''.join(tokens)


if __name__ == "__main__":

    # assert simplify("x*x*x+5*x*x+x*x+3*x-1") == "x**3+6*x**2+3*x-1"
    # assert simplify("-x*x*x+5*x*x+x*x+3*x-1") == "-x**3+6*x**2+3*x-1"

    assert simplify("(x-1)*(x+1)") == "x**2-1", "First and simple"

    # assert simplify("(x+1)*(x+1)") == "x**2+2*x+1", "Almost the same"
    # assert simplify("(x+3)*x*2-x*x") == "x**2+6*x", "Different operations"
    # assert simplify("x+x*x+x*x*x") == "x**3+x**2+x", "Don't forget about order"
    # assert simplify("(2*x+3)*2-x+x*x*x*x") == "x**4+3*x+6", "All together"
    # assert simplify("x*x-(x-1)*(x+1)-1") == "0", "Zero"
    # assert simplify("5-5-x") == "-x", "Negative C1"
    # assert simplify("x*x*x-x*x*x-1") == "-1", "Negative C0"
