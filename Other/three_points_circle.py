from typing import Iterable


def get_equation_string(x0, y0, r):
    def format_string(string):
        return f'{string:.2f}'.rstrip('0.')

    x0, y0, r = map(format_string, (x0, y0, r))
    equation_string = f'(x-{x0})^2+(y-{y0})^2={r}^2'
    return equation_string


def get_determinant(matrix, sub_determinants_mode=False):
    if len(matrix) == 1:
        while isinstance(matrix, Iterable):
            matrix = matrix[0]
        return matrix
    else:
        columns = list(zip(*matrix))

        determinant = 0
        sub_determinants = []
        for i, first_row_element in enumerate(matrix[0]):
            sub_columns = []
            for j, column in enumerate(columns):
                if j == i:
                    continue
                sub_columns.append(column[1:])
            sub_matrix = list(zip(*sub_columns))
            sub_determinant = get_determinant(sub_matrix)
            sub_determinants.append(sub_determinant)
            determinant_delta = pow(-1, i) * first_row_element * sub_determinant
            determinant += determinant_delta

    if sub_determinants_mode:
        return sub_determinants
    return determinant


def checkio(data):
    '''http://www.ambrsoft.com/TrigoCalc/Circle3D.htm'''

    print('Data:', data)

    digits = (int(''.join(l for l in part if l not in '()')) for part in data.split(','))

    matrix = [[0, 0, 0, 1]]
    for x, y in zip(digits, digits):
        print('X:', x)
        print('Y:', y)
        matrix.append([x ** 2 + y ** 2, x, y, 1])

    print('Matrix:')
    for row in matrix:
        print(row)

    sub_determinants = get_determinant(matrix, sub_determinants_mode=True)
    print('Sub determinants:', sub_determinants)

    a, b, c, d = (pow(-1, i) * sub_determinant for i, sub_determinant in enumerate(sub_determinants))
    print('A:', a)
    print('B:', b)
    print('C:', c)
    print('D:', d)

    x0 = -b / 2 / a
    y0 = -c / 2 / a
    r = pow((b ** 2 + c ** 2) / 4 / a ** 2 - d / a, 0.5)
    print('X0:', x0)
    print('Y0:', y0)
    print('R:', r)

    equation_string = get_equation_string(x0, y0, r)
    print('Equation string:', equation_string)
    print()
    return equation_string


if __name__ == '__main__':
    assert checkio("(2,2),(6,2),(2,6)") == "(x-4)^2+(y-4)^2=2.83^2"
    assert checkio("(3,7),(6,9),(9,7)") == "(x-6)^2+(y-5.75)^2=3.25^2"
    assert checkio("(1,1),(2,1),(1,2)") == "(x-1.5)^2+(y-1.5)^2=0.71^2"
