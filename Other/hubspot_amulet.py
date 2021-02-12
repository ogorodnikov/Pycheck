TARGET_ANGLES = [0, 225, 315]


def egcd(a, b):
    """ https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm """

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    print('A, B:', a, b)
    print('Old remainder = GCD:', old_r)
    print('Old S, Old T = Bézout coefficients:', old_s, old_t)
    print('a * x + b * y = d')
    print(f'{a} * {old_s} + {b} * {old_t} = {old_r}')
    print()
    return old_r, old_s


def get_determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    determinant = 0
    for i, first_row_element in enumerate(matrix[0]):
        sub_matrix = [row[:i] + row[i + 1:] for row in matrix[1:]]
        sub_determinant = get_determinant(sub_matrix)
        determinant_delta = pow(-1, i) * first_row_element * sub_determinant
        determinant += determinant_delta
    return determinant


def checkio(matrix):
    print('Matrix:')
    for row in matrix:
        print(row)
    print()

    transposed_matrix = list(zip(*matrix))

    matrices = [transposed_matrix]
    for i in range(3):
        new_matrix = matrix.copy()
        new_matrix[i] = TARGET_ANGLES
        new_transposed_matrix = list(zip(*new_matrix))
        matrices.append(new_transposed_matrix)
    print('Matrices:')
    for m in matrices:
        for row in m:
            print(row)
        print()

    determinants = list(map(get_determinant, matrices))
    print('Determinants:', determinants)

    # modular inverse of the determinant to get 1/d
    gcd, bezout_s = egcd(determinants[0], 360)
    print('GCD:', gcd)
    print('Bézout S:', bezout_s)

    idm = bezout_s % (360 // gcd)
    print('IDM:', idm)

    angles = [(idm * determinant // gcd + 180) % 360 - 180 for determinant in determinants[1:]]
    print('Angles:', angles)
    print()
    return angles


if __name__ == '__main__':
    def check_it(func, matrix):
        result = func(matrix)
        if not all(-180 <= el <= 180 for el in result):
            print("The angles must be in range from -180 to 180 inclusively.")
            return False
        f, s, t = result
        temp = [0, 0, 0]
        temp[0] += f
        temp[1] += matrix[0][1] * f
        temp[2] += matrix[0][2] * f

        temp[0] += matrix[1][0] * s
        temp[1] += s
        temp[2] += matrix[1][2] * s

        temp[0] += matrix[2][0] * t
        temp[1] += matrix[2][1] * t
        temp[2] += t
        temp = [n % 360 for n in temp]
        if temp == [0, 225, 315]:
            return True
        else:
            print("This is the wrong final position {0}.".format(temp))
            return False


    assert check_it(checkio,
                    [[1, 2, 3],
                     [3, 1, 2],
                     [2, 3, 1]]), "1st example"
    assert check_it(checkio,
                    [[1, 3, 2],
                     [2, 1, 3],
                     [3, 2, 1]]), "1st example"
    assert check_it(checkio,
                    [[1, 4, 2],
                     [2, 1, 2],
                     [2, 2, 1]]), "2nd example"
    assert check_it(checkio,
                    [[1, 2, 5],
                     [2, 1, 1],
                     [2, 5, 1]]), "3rd example"
    assert check_it(checkio,
                    [[1, 5, 2],
                     [2, 1, 7],
                     [1, 3, 1]])
    assert check_it(checkio,
                    [[1, 3, 5],
                     [3, 1, 5],
                     [2, 5, 1]])
