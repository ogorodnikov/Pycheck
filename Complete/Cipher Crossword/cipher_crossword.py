from collections import defaultdict
from contextlib import contextmanager

WORD_LOCATION_PATTERN = ([[1, 4], [1], [1, 5], [1], [1, 6]],
                         [[4],    [],  [5],    [],  [6]],
                         [[2, 4], [2], [2, 5], [2], [2, 6]],
                         [[4],    [],  [5],    [],  [6]],
                         [[3, 4], [3], [3, 5], [3], [3, 6]])
EMPTY_LETTER = ' '


@contextmanager
def get_word_coordinates(word_location_pattern):
    try:
        max_word_number = max(max(max(element for element in cell) if cell else 0
                                  for cell in row)
                              for row in word_location_pattern)
        word_coordinates = defaultdict(list)
        for word_number in range(max_word_number + 1):
            for y in range(len(word_location_pattern)):
                for x in range(len(word_location_pattern[0])):
                    if word_number in word_location_pattern[y][x]:
                        word_coordinates[word_number].append((x, y))
        yield word_coordinates
    finally:
        pass


def print_table(table):
    if not table:
        print('Empty table')
        return
    element_width = max(max(len(str(element)) for element in row) for row in table)
    for row in table:
        print(''.join(f'{element:{element_width + 1}}' for element in row))


def checkio(crossword, words):
    with get_word_coordinates(WORD_LOCATION_PATTERN) as word_coordinates:
        print('Word coordinates:', word_coordinates)
        print('Crossword:')
        print_table(crossword)

        finished_crossword = []
        populated_crossword = [[EMPTY_LETTER for _ in row] for row in crossword]
        letter_codes = defaultdict(int)
        unused_words = set(words)

        q = [(populated_crossword, letter_codes, unused_words)]
        while q:
            populated_crossword, letter_codes, unused_words = q.pop()

            for number, coordinates in word_coordinates.items():
                # print('Number:', number)
                new_letter_codes = letter_codes.copy()

                for word in unused_words.copy():
                    # print('    Word:', word)
                    new_unused_words = unused_words.copy()
                    new_populated_crossword = [[letter for letter in row] for row in populated_crossword]
                    if len(word) != len(coordinates):
                        # print('Length does not match')
                        continue
                    is_misfit = False
                    for i, letter in enumerate(word):
                        if is_misfit:
                            break
                        x, y = coordinates[i]
                        # print('        Coordinates:', (x, y))
                        code = crossword[y][x]
                        # print('        Letter:     ', letter)
                        # print('        Code:       ', code)

                        for stored_letter, stored_code in new_letter_codes.items():
                            if code == stored_code and letter != stored_letter:
                                # print(f'        - Code {stored_code} already used for {stored_letter}')
                                is_misfit = True
                                break
                        if new_populated_crossword[y][x] != EMPTY_LETTER:
                            if new_populated_crossword[y][x] != letter:
                                # print(f'        - Pos {(x, y)} already used by letter {populated_crossword[y][x]}')
                                is_misfit = True
                                break

                        new_letter_codes[letter] = code
                        new_populated_crossword[y][x] = letter

                    if not is_misfit:
                        new_unused_words -= {word}
                        q.append((new_populated_crossword, dict(new_letter_codes), new_unused_words))
                        # print('> Pushing:', (new_populated_crossword, dict(new_letter_codes), new_unused_words))

                    if new_unused_words == set():
                        completed_crossword = new_populated_crossword

        print('Completed crossword:')
        print_table(completed_crossword)

    return completed_crossword


if __name__ == '__main__':
    assert checkio(
        [
            [21, 6, 25, 25, 17],
            [14, 0, 6, 0, 2],
            [1, 11, 16, 1, 17],
            [11, 0, 16, 0, 5],
            [26, 3, 14, 20, 6]
        ],
        ['hello', 'habit', 'lemma', 'ozone', 'bimbo', 'trace']) == [['h', 'e', 'l', 'l', 'o'],
                                                                    ['a', ' ', 'e', ' ', 'z'],
                                                                    ['b', 'i', 'm', 'b', 'o'],
                                                                    ['i', ' ', 'm', ' ', 'n'],
                                                                    ['t', 'r', 'a', 'c', 'e']]
