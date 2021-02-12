FIRST_TEN = ["one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):
    print('Number:', number)
    ones, tens, hundreds = (number % pow(10, power + 1) // pow(10, power) for power in range(3))
    print('Digit positions:', hundreds, tens, ones)

    phrase_parts = []
    if hundreds:
        phrase_parts.extend((FIRST_TEN[hundreds - 1], HUNDRED))
    if tens == 1:
        phrase_parts.append(SECOND_TEN[ones])
    elif tens > 1:
        phrase_parts.append(OTHER_TENS[tens - 2])
    if ones and tens != 1:
        phrase_parts.append(FIRST_TEN[ones - 1])

    print('Phrase parts:', phrase_parts)
    phrase = ' '.join(phrase_parts)
    print('Phrase:', phrase)
    print()
    return phrase


if __name__ == '__main__':
    assert checkio(4)  == 'four', "1st example"
    assert checkio(133) == 'one hundred thirty three', "2nd example"
    assert checkio(12) == 'twelve', "3rd example"
    assert checkio(101) == 'one hundred one', "4th example"
    assert checkio(212) == 'two hundred twelve', "5th example"
    assert checkio(40) == 'forty', "6th example"
    assert not checkio(212).endswith(' '), "Don't forget strip whitespaces at the end of string"
