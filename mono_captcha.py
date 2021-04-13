from itertools import starmap
from operator import sub
from typing import List

SPACE_WIDTH = 1
SYMBOL_WIDTH = 3
MARK = 'X'

FONT = ("--X--XXX-XXX-X-X-XXX--XX-XXX-XXX--XX-XX--",
        "-XX----X---X-X-X-X---X-----X-X-X-X-X-X-X-",
        "--X---XX--X--XXX-XX--XXX--X--XXX-XXX-X-X-",
        "--X--X-----X---X---X-X-X-X---X-X---X-X-X-",
        "--X--XXX-XXX---X-XX---XX-X---XXX-XX---XX-")


def parse_image(image):
    return list(zip(*([row[i + SPACE_WIDTH:i + SPACE_WIDTH + SYMBOL_WIDTH]
                       for i in range(0, len(row) - SPACE_WIDTH, SYMBOL_WIDTH + SPACE_WIDTH)]
                      for row in image)))


def strings_to_binary(strings):
    return [[[1 if cell == MARK else 0 for cell in list(line)]
             for line in number]
            for number in strings]


def checkio(image: List[List[int]]) -> int:
    template_strings = parse_image(FONT)

    template_images = strings_to_binary(template_strings)

    symbol_images = parse_image(image)

    digits = [min((sum(sum(map(abs, starmap(sub, zip(*line_pair))))
                       for line_pair in zip(symbol, template)), digit)
                  for digit, template in enumerate(template_images, 1))[1]
              for symbol in symbol_images]

    number = sum(digit * 10 ** position for position, digit in (enumerate(reversed(digits))))

    print('Image:')
    [print(''.join(MARK if cell == 1 else ' ' for cell in line)) for line in image]

    # print('FONT:', FONT)
    # print('Template strings:', template_strings)
    # print('Template images:', template_images)
    # print('Symbol images:', symbol_images)
    # print('Digits:', digits)
    print('Number:', number)
    print()
    return number


if __name__ == '__main__':
    # assert checkio([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
    #                 [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    #                 [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    #                 [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    #                 [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, "394 clear"
    # assert checkio([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    #                 [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    #                 [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    #                 [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    #                 [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, "again 394 but with noise"

    assert checkio(
        [[0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
         [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
         [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]])
