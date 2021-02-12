from itertools import permutations

TARGET_ANGLES = [0, 225, 315]


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
    """ Calculate:
          angles for 3 levers
        Input:
          cross-dependence of levers is defined by matrix
          resulting lever positions are TARGET_ANGLES
        Using:
        - permutations of additional_angles for target angles
        - Cramer's rule
        - shift of resulting angles
    """
    print('Matrix:')
    for row in matrix:
        print(row)
    print()

    transposed_matrix = list(zip(*matrix))

    additional_angles = [360 * i for i in range(10)]
    print('Additional angles:', additional_angles)

    additional_angles_permutations = list(permutations(additional_angles, 3))
    print('Additional angles permutations:', additional_angles_permutations)

    for permutation_index, additional_angles_permutation in enumerate(additional_angles_permutations):
        print('Additional angles permutation:', additional_angles_permutation)

        target_angles_with_addition = [angle + additional_angle
                                       for angle, additional_angle
                                       in zip(TARGET_ANGLES, additional_angles_permutation)]
        print('Target angles with addition:', target_angles_with_addition)

        matrices = [transposed_matrix]
        for i in range(3):
            new_matrix = matrix.copy()
            new_matrix[i] = target_angles_with_addition
            new_transposed_matrix = list(zip(*new_matrix))
            matrices.append(new_transposed_matrix)
        print('Matrices:')
        for m in matrices:
            for row in m:
                print(row)
            print()

        determinants = list(map(get_determinant, matrices))
        print('Determinants:', determinants)

        main_determinant = determinants[0]
        print('Main determinant:', main_determinant)

        angles = [determinant / main_determinant for determinant in determinants[1:]]
        print('Angles:', angles)

        for shift in (360 * i for i in range(-3, 3)):
            angles_with_shift = [angle + shift for angle in angles]
            if all(-180 < angle < 180 and int(angle) == angle for angle in angles_with_shift):
                resulting_angles = [int(angle) for angle in angles_with_shift]
                print('Resulting angles:', resulting_angles)
                print('Additional angles permutation:', additional_angles_permutation)
                print('Permutation index:', permutation_index, 'out of', len(additional_angles_permutations))
                print('Shift:', shift)
                print()
                return resulting_angles

    print('No angles filtered')
    return None


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
