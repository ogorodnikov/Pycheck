from itertools import repeat, starmap, chain
from operator import floordiv, truediv

NUMBERS = {
    0: 'zero',
    1: "one",          10**12: "trillion",
    2: "two",          10**15: "quadrillion",
    3: "three",        10**18: "quintillion",
    4: "four",         10**21: "sextillion",
    5: "five",         10**24: "septillion",
    6: "six",          10**27: "octillion",
    7: "seven",        10**30: "nonillion",
    8: "eight",        10**33: "decillion",
    9: "nine",         10**36: "undecillion",
    10: "ten",         10**39: "duodecillion",
    11: "eleven",      10**42: "tredecillion",
    12: "twelve",      10**45: "quattuordecillion",
    13: "thirteen",    10**48: "quinquadecillion",
    14: "fourteen",    10**51: "sedecillion",
    15: "fifteen",     10**54: "septendecillion",
    16: "sixteen",     10**57: "octodecillion",
    17: "seventeen",   10**60: "novendecillion",
    18: "eighteen",    10**63: "vigintillion",
    19: "nineteen",    10**66: "unvigintillion",
    20: "twenty",      10**69: "duovigintillion",
    30: "thirty",      10**72: "tresvigintillion",
    40: "forty",       10**75: "quattuorvigintillion",
    50: "fifty",       10**78: "quinquavigintillion",
    60: "sixty",       10**81: "sesvigintillion",
    70: "seventy",     10**84: "septemvigintillion",
    80: "eighty",      10**87: "octovigintillion",
    90: "ninety",      10**90: "novemvigintillion",
    100: "hundred",    10**93: "trigintillion",
    10**3: "thousand", 10**96: "untrigintillion",
    10**6: "million",  10**99: "duotrigintillion",
    10**9: "billion",  10**100: "googol"
}


def checkio(number):
    if number in NUMBERS and number < 100:
        return NUMBERS[number]

    biggest_divisor = next(divisor for divisor in sorted(NUMBERS)[::-1] if number//divisor)
    # biggest_divisor = next(filter(lambda divisor: number//divisor, reversed(sorted(NUMBERS))))

    quotient, remainder = divmod(number, biggest_divisor)
    prefix = [checkio(quotient)] * (number >= 100)
    postfix = [checkio(remainder)] * (remainder > 0)
    phrase = prefix + [NUMBERS[biggest_divisor]] + postfix
    print('Phrase:', ' '.join(phrase))
    return ' '.join(phrase)


if __name__ == '__main__':
    assert checkio(90670)