import re


def simplify(expr):
    print('Expr:', expr)

    terms = re.findall(r'([+-].+?)(?=[+-]|$)', expr)
    print('Terms:', terms)

    quit()


    return expr

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

    assert simplify("-5*x*x+3*x-1") == "-5*x**2+3*x-1"

    # assert simplify("(x-1)*(x+1)") == "x**2-1", "First and simple"

    # assert simplify("(x+1)*(x+1)") == "x**2+2*x+1", "Almost the same"
    # assert simplify("(x+3)*x*2-x*x") == "x**2+6*x", "Different operations"
    # assert simplify("x+x*x+x*x*x") == "x**3+x**2+x", "Don't forget about order"
    # assert simplify("(2*x+3)*2-x+x*x*x*x") == "x**4+3*x+6", "All together"
    # assert simplify("x*x-(x-1)*(x+1)-1") == "0", "Zero"
    # assert simplify("5-5-x") == "-x", "Negative C1"
    # assert simplify("x*x*x-x*x*x-1") == "-1", "Negative C0"