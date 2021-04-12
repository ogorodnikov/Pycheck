import re
from collections import defaultdict, Counter
from itertools import product


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


def tokenize(expression):
    print('>>>> Tokenize:', expression)

    def process_mult(_, token):
        return 'Mult', token

    def process_add(_, token):
        return 'Add', token

    def process_sub(_, token):
        return 'Sub', token

    def process_number(_, token):
        return 'Poly', {0: int(token)}

    def process_x(_, token):
        return 'Poly', {1: 1}

    bracket_level = -1

    def process_open_bracket(_, token):
        nonlocal bracket_level
        bracket_level += 1

        return 'Open bracket', bracket_level

    def process_close_bracket(_, token):
        nonlocal bracket_level
        bracket_level -= 1

        return 'Close bracket', bracket_level + 1

    scanner = re.Scanner([(r'\(', process_open_bracket),
                          (r'\)', process_close_bracket),
                          (r'\*', process_mult),
                          (r'\+', process_add),
                          (r'-', process_sub),
                          (r'\d+', process_number),
                          (r'x', process_x)])

    tokens, unrecognised = scanner.scan(expression)

    # print('Tokens:')
    # [print(token) for token in tokens]
    # print()

    return tokens


def reduce_polynomial(tokens):

    print('>>>> Reduce:', tokens)

    while any(token_type == 'Open bracket' for token_type, token_value in tokens):

        last_bracket_index = 0

        for token_index, (token_type, token_value) in enumerate(tokens):

            print(token_index, (token_type, token_value))

            if token_type == 'Open bracket':
                last_bracket_index = token_index

            if token_type == 'Close bracket':

                sub_expression = tokens[last_bracket_index + 1:token_index]

                print('    Sub-expression:', sub_expression)

                tokens = tokens[:last_bracket_index] + reduce_polynomial(sub_expression) + tokens[token_index + 1:]
                print('Tokens after sub-expression:', tokens)
                break

    while any(token_type == 'Mult' for token_type, token_value in tokens):

        for token_index, (token_type, token_value) in enumerate(tokens):

            if token_type == 'Mult':

                _, a_poly = tokens[token_index - 1]
                _, b_poly = tokens[token_index + 1]

                c_poly = multiply_poly(a_poly, b_poly)

                tokens = tokens[:token_index - 1] + [('Poly', c_poly)] + tokens[token_index + 2:]
                print('Tokens after mult:', tokens)
                break

    while any(token_type == 'Add' for token_type, token_value in tokens):

        for token_index, (token_type, token_value) in enumerate(tokens):

            if token_type == 'Add':

                _, a_poly = tokens[token_index - 1]
                _, b_poly = tokens[token_index + 1]

                c_poly = add_poly(a_poly, b_poly)

                tokens = tokens[:token_index - 1] + [('Poly', c_poly)] + tokens[token_index + 2:]
                print('Tokens after add:', tokens)
                break

    while any(token_type == 'Sub' for token_type, token_value in tokens):

        for token_index, (token_type, token_value) in enumerate(tokens):

            if token_type == 'Sub':

                _, a_poly = tokens[token_index - 1]
                _, b_poly = tokens[token_index + 1]

                c_poly = sub_poly(a_poly, b_poly)

                tokens = tokens[:token_index - 1] + [('Poly', c_poly)] + tokens[token_index + 2:]
                break

    print('==== Tokens:', tokens)
    print()
    input()

    return tokens


def multiply_poly(a_poly, b_poly):
    # print('A:', a_poly)
    # print('B:', b_poly)

    pairs = list(product(a_poly.items(), b_poly.items()))
    # print('Pairs:', pairs)

    terms = []

    for pair in pairs:
        (u_degree, u_coefficient), (v_degree, v_coefficient) = pair
        term = (u_degree + v_degree, u_coefficient * v_coefficient)
        terms.append(term)

        # print('    Pair:', pair)
        # print('    Term:', term)

    # print('Terms:', terms)

    c_poly = defaultdict(int)
    for term in terms:
        term_degree, term_coefficient = term
        c_poly[term_degree] += term_coefficient

    return dict(c_poly)


def add_poly(a_poly, b_poly):

    degrees = set(a_poly.keys()) | set(b_poly.keys())

    a_dict = defaultdict(int)
    b_dict = defaultdict(int)
    a_dict.update(a_poly)
    b_dict.update(b_poly)

    c_poly = {degree: a_dict[degree] + b_dict[degree] for degree in degrees}

    # print('A:', a_poly)
    # print('B:', b_poly)
    # print('Degrees:', degrees)
    # print('C poly:', c_poly)

    return c_poly


def sub_poly(a_poly, b_poly):

    degrees = set(a_poly.keys()) | set(b_poly.keys())

    a_dict = defaultdict(int)
    b_dict = defaultdict(int)
    a_dict.update(a_poly)
    b_dict.update(b_poly)

    c_poly = {degree: a_dict[degree] - b_dict[degree] for degree in degrees}

    # print('A:', a_poly)
    # print('B:', b_poly)
    # print('Degrees:', degrees)
    # print('C poly:', c_poly)

    return c_poly


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

    tokens = tokenize(expr)
    resulting_polynomial = reduce_polynomial(tokens)

    # resulting_polynomial_string = polynomial_to_string(resulting_polynomial)
    #
    # print('Resulting polynomial string:', resulting_polynomial_string)
    # print()
    # return resulting_polynomial_string


if __name__ == "__main__":

    assert simplify("((x*5)*(x+1))-16456*x*x*x+(x*x)*(1)")

    # assert simplify("x*x*x+5*x*x+x*x+3*x-1") == "x**3+6*x**2+3*x-1"
    # assert simplify("-x*x*x+5*x*x+x*x+3*x-1") == "-x**3+6*x**2+3*x-1"

    # assert simplify("(x-1)*(x+1)") == "x**2-1", "First and simple"
    # assert simplify("(x+1)*(x+1)") == "x**2+2*x+1", "Almost the same"
    # assert simplify("(x+3)*x*2-x*x") == "x**2+6*x", "Different operations"
    # assert simplify("x+x*x+x*x*x") == "x**3+x**2+x", "Don't forget about order"
    # assert simplify("(2*x+3)*2-x+x*x*x*x") == "x**4+3*x+6", "All together"
    # assert simplify("x*x-(x-1)*(x+1)-1") == "0", "Zero"
    # assert simplify("5-5-x") == "-x", "Negative C1"
    # assert simplify("x*x*x-x*x*x-1") == "-1", "Negative C0"
