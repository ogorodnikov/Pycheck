from typing import Tuple, Dict, List


def undead(house_plan: Tuple[str, ...],
           monsters: Dict[str, int],
           counts: Dict[str, List[int]]) -> Tuple[str, ...]:
    return house_plan


if __name__ == '__main__':
    TESTS = (
        (
            ('. \\ . /',
             '\\ . . .',
             '/ \\ . \\',
             '. \\ / .'),
            {'ghost': 2, 'vampire': 2, 'zombie': 4},
            {'E': [0, 3, 0, 1],
             'N': [3, 0, 3, 0],
             'S': [2, 1, 1, 4],
             'W': [4, 0, 0, 0]},
            ('Z \\ V /',
             '\\ Z G V',
             '/ \\ Z \\',
             'G \\ / Z'),
        ),
        (
            ('\\ . . .',
             '. . \\ /',
             '/ \\ . \\',
             '/ . \\ \\',
             '. . . .',
             '/ / . /'),
            {'ghost': 3, 'vampire': 5, 'zombie': 4},
            {'E': [1, 0, 0, 3, 4, 0],
             'N': [2, 1, 2, 0],
             'S': [0, 3, 3, 0],
             'W': [0, 3, 0, 0, 4, 2]},
            ('\\ G V G',
             'V G \\ /',
             '/ \\ Z \\',
             '/ V \\ \\',
             'Z V Z Z',
             '/ / V /'),
        ),
        (
            ('. . . / . . /',
             '. . \\ / . . .',
             '. . . . . . .',
             '. \\ . . . / \\',
             '. / . \\ . . \\'),
            {'ghost': 6, 'vampire': 10, 'zombie': 9},
            {'E': [0, 4, 6, 0, 1],
             'N': [3, 5, 0, 3, 3, 7, 1],
             'S': [3, 0, 5, 0, 3, 0, 3],
             'W': [2, 4, 6, 0, 2]},
            ('Z Z G / V V /',
             'Z Z \\ / G V V',
             'G Z Z V Z Z V',
             'G \\ Z V V / \\',
             'V / V \\ G G \\'),
        ),
    )

    for test_nb, (house_plan, monsters, counts, answer) in enumerate(TESTS, 1):
        result = tuple(undead(house_plan, monsters, counts))
        if result != answer:
            print(f'You failed the test #{test_nb}:',
                  *house_plan, monsters, counts,
                  'Your result:', *result,
                  'Right answer:', *answer,
                  sep='\n')
            break
    else:
        print('Well done! Click on "Check" for more tests.')