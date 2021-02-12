DIGITS = {0: '0001101',
          1: '0011001',
          2: '0010011',
          3: '0111101',
          4: '0100011',
          5: '0110001',
          6: '0101111',
          7: '0111011',
          8: '0110111',
          9: '0001011'}

ZERO_DIGIT = {0: 'LLLLLL',
              1: 'LLGLGG',
              2: 'LLGGLG',
              3: 'LLGGGL',
              4: 'LGLLGG',
              5: 'LGGLLG',
              6: 'LGGGLL',
              7: 'LGLGLG',
              8: 'LGLGGL',
              9: 'LGGLGL'}


def check_guard_bars(barcode):
    left_guard_bar = barcode[0:3]
    center_guard_bar = barcode[3 + 6 * 7: 3 + 6 * 7 + 5]
    right_guard_bar = barcode[3 + 6 * 7 + 5 + 6 * 7: 3 + 6 * 7 + 5 + 6 * 7 + 3]

    print('Left guard bar:', left_guard_bar)
    print('Center guard bar:', center_guard_bar)
    print('Right guard bar:', right_guard_bar)

    if left_guard_bar != '_ _':
        print('Wrong left guard bar')
        raise ValueError
    if center_guard_bar != ' _ _ ':
        print('Wrong center guard bar')
        raise ValueError
    if right_guard_bar != '_ _':
        print('Wrong Right guard bar')
        raise ValueError


def decode_barcode(barcode_parts, code_table):
    print('Decoding:')
    digits = []
    letters = ''
    for barcode_part in barcode_parts:

        binary_part = barcode_part.translate({ord('_'): ord('1'), ord(' '): ord('0')})
        print('Barcode part: ', barcode_part)
        print('Binary part:', binary_part)

        is_pattern_matched = False
        for letter in code_table:
            for digit, binary_pattern in code_table[letter].items():
                if binary_part == binary_pattern:
                    print('    Matched digit:', digit)
                    print('    Matched letter:', letter)
                    is_pattern_matched = True
                    digits.append(digit)
                    letters += letter
        if not is_pattern_matched:
            print('No patterns matched')

    return digits, letters


def barcode_reader(barcode):
    print('Barcode:', barcode)

    try:
        check_guard_bars(barcode)
    except ValueError:
        print()
        return None

    code_table = {code: dict() for code in 'LGR'}
    for digit in DIGITS:
        l_code = DIGITS[digit]
        r_code = l_code.translate({ord('0'): ord('1'), ord('1'): ord('0')})
        g_code = r_code[::-1]

        code_table['L'][digit] = l_code
        code_table['G'][digit] = g_code
        code_table['R'][digit] = r_code

    print('Code table:')
    for letter in code_table:
        print(letter, code_table[letter])

    barcode_left = [barcode[3 + offset * 7: 10 + offset * 7] for offset in range(6)]
    barcode_right = [barcode[3 + 6 * 7 + 5 + offset * 7: 10 + 6 * 7 + 5 + offset * 7] for offset in range(6)]

    print('Barcode parts:')
    print('Left:')
    for barcode_part in barcode_left:
        print(barcode_part)
    print('Right:')
    for barcode_part in barcode_right:
        print(barcode_part)

    if (not all(barcode_part[0] == ' ' for barcode_part in barcode_left) or
            not all(barcode_part[0] == '_' for barcode_part in barcode_right)):
        print('First symbols mismatch')
        return None

    barcode_parts = barcode_left + barcode_right
    digits, letters = decode_barcode(barcode_parts, code_table)
    print('Letters:', letters)

    if letters.startswith('GGGGGG'):
        reversed_barcode_parts = [right_part[::-1] for right_part in reversed(barcode_right)]
        reversed_barcode_parts += [left_part[::-1] for left_part in reversed(barcode_left)]
        print('Barcode parts:', barcode_parts)
        print('Reversed barcode parts:', reversed_barcode_parts)
        digits, letters = decode_barcode(reversed_barcode_parts, code_table)
        print('Letters:', letters)

    if len(letters) < 12:
        print('Letters length mismatch')
        return None

    zero_digit = (digit for digit, pattern in ZERO_DIGIT.items() if letters[:6] == pattern)
    digits.insert(0, *zero_digit)

    odd_digits = digits[::2]
    even_digits = digits[1::2]
    print('Odd digits:', odd_digits)
    print('Even digits:', even_digits)

    control_sum = sum(odd_digits) + 3 * sum(even_digits)
    print('Control sum:', control_sum)
    control_sum_mismatch = control_sum % 10

    if control_sum_mismatch:
        print('Control sum mismatch:', control_sum_mismatch)
        print()
        return None

    digit_string = ''.join(map(str, digits))
    print('Digit string:', digit_string)
    print()
    return digit_string


if __name__ == '__main__':
    assert barcode_reader(
        '_ _   _ __ _  ___ __  __  _  __ ____ _  ___ _ _ _ __  __ __ __  _    _ _ ___  _  ___ _   _  _ _'
    ) == '5901234123457', '5901234123457'

    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) == '4299687613665', '4299687613665'

    assert barcode_reader(
        '_ _ ___ __  __  _  _  __ ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __ __  _ _'
    ) is None, '0712345678912 : wrong check digit (right: 1)'

    assert barcode_reader(
        '___  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) is None, 'wrong left guard bar'

    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ ___ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) is None, 'wrong center bar'

    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ ___'
    ) is None, 'wrong right guard bar'

    assert barcode_reader(
        "_ _ __  __ __  __  _ ___   _  _  _   _    _ _ _ _ _   __ __   _ _ ____ __  _  _  __  __ ___ _ _"
    ) == '0712345678911'

    assert barcode_reader(
        "_ _ ___ __  __  _        ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __  __ _ _"
    ) is None

    assert barcode_reader(
        "_ _ ___  _  _   _  ___ _ _    _  ___ _  __ __ _ _ __  _  __ __  _  ___ _ _    _   __ __   _ _ _"
    ) == '3456522243475'
