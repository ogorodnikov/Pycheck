from itertools import zip_longest


def int_to_base(number, base):
    digits = []
    digit_width = len(str(base - 1))
    while number:
        number, digit = divmod(number, base)
        digits.append(f'{digit:0{digit_width}}')
    return digits[::-1] or ['0']


def power_form(digits, decimals, powers, base):
    print('Digits:', digits)
    print('Powers:', powers)

    power_tuples = list(zip_longest(powers, reversed(digits)))[::-1]
    print('Power tuples:', power_tuples)

    whole_part = ''
    fractional_part = ''
    selected_power = None
    is_whole_part = True
    for power, digit in power_tuples:
        print('    Power tuple:', (power, digit))
        if digit is None:
            continue
        if is_whole_part:
            whole_part += digit
        if not is_whole_part:
            fractional_part += digit.lstrip('0')
        if power is not None and selected_power is None:
            selected_power = power
            is_whole_part = False

    if decimals == 0:
        fractional_part = ''

    if base <= 10:
        whole_part = str(int(whole_part or '0', base))
        fractional_part = str(int(fractional_part or '0', base))

    print('Selected power:', selected_power)
    print('Whole part:', whole_part)
    print('Fractional part:', fractional_part)

    number = float(whole_part + '.' + fractional_part)
    print('Float:', number)
    print('Decimals:', decimals)

    power_number = f'{number:.{decimals}f}' + selected_power
    print('Power number:', power_number)

    return power_number


def friendly_number(number, base=1000, decimals=0, suffix='',
                    powers=('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')):
    print('Initial number:', f'{number:,}')
    print('Base:', base)

    is_negative = number < 0
    if is_negative:
        unsigned_number = -number
    else:
        unsigned_number = number
    print('Unsigned number:', unsigned_number)

    digits = int_to_base(unsigned_number, base)
    print('Digits:', digits)
    print('Based:', ''.join(map(str, digits)))

    powered_number = power_form(digits, decimals, powers, base)
    signed_number = '-' * is_negative + powered_number
    final_number = signed_number + suffix
    print('Sign and suffix:', final_number)
    print()
    return final_number


if __name__ == '__main__':
    assert friendly_number(102) == '102', '102'
    assert friendly_number(10240) == '10k', '10k'
    assert friendly_number(12341234, decimals=1) == '12.3M', '12.3M'
    assert friendly_number(12461, decimals=1) == '12.5k', '12.5k'
    assert friendly_number(1024000000, base=1024, suffix='iB') == '976MiB', '976MiB'

    assert friendly_number(-150, base=100, powers=["", "d", "D"]) == '-1d'
    assert friendly_number(255000000000, powers=["", "k", "M"]) == '255000M'
    assert friendly_number(10 ** 32) == '100000000Y'
    assert friendly_number(-155, base=100, decimals=1, powers=["", "d", "D"]) == '-1.6d'
    assert friendly_number(0, decimals=3, suffix="th")
    assert friendly_number(4294967297, base=2,
                           powers=["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12",
                                   "p13",
                                   "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p25",
                                   "p26",
                                   "p27", "p28", "p29", "p30", "p31"]) == '2p31'
    assert friendly_number(4000000001, base=1024, decimals=1) == '3.7G'

