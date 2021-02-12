from itertools import combinations_with_replacement, product

DIGITS = {1: ('B', 'C'),
          2: ('A', 'B', 'G', 'E', 'D'),
          3: ('A', 'B', 'G', 'C', 'D'),
          4: ('F', 'G', 'B', 'C'),
          5: ('A', 'F', 'G', 'C', 'D'),
          6: ('A', 'F', 'G', 'C', 'D', 'E'),
          7: ('A', 'B', 'C'),
          8: ('A', 'B', 'C', 'D', 'E', 'F', 'G'),
          9: ('A', 'B', 'C', 'D', 'F', 'G'),
          0: ('A', 'B', 'C', 'D', 'E', 'F')}


def seven_segment(lit_seg, broken_seg):

    print('Lightened segments:', lit_seg)
    print('Broken segments:', broken_seg)

    combination_set = set(map(frozenset, combinations_with_replacement(set(broken_seg) | {''}, len(broken_seg) + 1)))
    combination_list = sorted(map(list, combination_set), key=lambda combination: (len(combination), combination))

    # print()
    # print('Combinations with replacement:')
    # for combination in combination_list:
    #     print(combination)

    digit_combinations = [sorted(list(lit_seg) + combination) for combination in combination_list]
    # print()
    # print('Digit combinations:')
    upper_digits = set()
    lower_digits = set()

    for combination in digit_combinations:
        upper_segments = set(segment for segment in combination if segment.isupper())
        lower_segments = set(segment.upper() for segment in combination if segment.islower())
        # print()
        # print('Combination:', combination)
        # print('Upper segments:', upper_segments)
        # print('Lower segments:', [segment.lower() for segment in lower_segments])
        for digit, digit_segments in DIGITS.items():
            if upper_segments == set(digit_segments):
                upper_digits.add(digit)
            if lower_segments == set(digit_segments):
                lower_digits.add(digit)



    print()
    print('Upper digits:', upper_digits)
    print('Lower digits:', lower_digits)
    possible_digits = [''.join(map(str, digits)) for digits in product(upper_digits, lower_digits)]
    print('Possible digits:', possible_digits)
    possible_digits_len = len(possible_digits)
    print('Possible digits length:', possible_digits_len)
    print()
    return possible_digits_len


if __name__ == '__main__':
    # assert seven_segment([], ["A","B","C", 'D', "E", "F", "G", "a", "b", "c", "d", "e", "f", "g"]) == 100
    assert seven_segment({'B', 'C', 'b', 'c'}, {'A'}) == 2, '11, 71'
    assert seven_segment({'B', 'C', 'a', 'f', 'g', 'c', 'd'}, {'A', 'G', 'D', 'e'}) == 6, '15, 16, 35, 36, 75, 76'
    assert seven_segment({'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f'}, {'G', 'g'}) == 4  # 0, 8, 80, 88
    assert seven_segment({'B', 'C', 'a', 'f', 'g', 'c', 'd'}, {'A', 'G', 'D', 'F', 'b', 'e'}) == 20, '15...98'
