from cmath import phase, polar, exp, cos, sin, pi, rect
from collections import defaultdict
from typing import Tuple, Dict, List


class Board:
    EMPTY = '.'
    MIRRORS = '\\/'

    def __init__(self, house_plan, monsters, counts):
        plan = [row.replace(' ', '') for row in house_plan]
        print('Plan:', plan)
        self.plan = plan
        self.height = len(plan)
        self.width = len(plan[0])

        self.all_cells = {complex(y, x): plan[y][x]
                          for y in range(self.height)
                          for x in range(self.width)}

        self.empty_cells = {cell for cell in self.all_cells
                            if self.all_cells[cell] in self.EMPTY}

        self.mirror_cells = {cell for cell in self.all_cells
                             if self.all_cells[cell] in self.MIRRORS}

        perimeter_coordinates = {'N': [complex(0, x) for x in range(self.width)],
                                 'W': [complex(y, 0) for y in range(self.height)],
                                 'S': [complex(self.height - 1, x) for x in range(self.width)],
                                 'E': [complex(y, self.width - 1) for y in range(self.height)]}

        paths = defaultdict(dict)

        for starting_direction, direction_name in zip((-1j, 1, -1, 1j), 'ENSW'):
            print('Direction name starting direction:', direction_name, starting_direction)

            angle = pi / 4

            for a in 1, 1j, -1, -1j:
                b = (a * exp(1j * -angle)).conjugate() * exp(1j * angle)
                c = (a * (cos(-angle) + 1j * sin(-angle))).conjugate() * (cos(angle) + 1j * sin(angle))

                a_phase = phase(a)
                a_modulus = abs(a)

                # print('A phase:', a_phase)
                # print('A modulus:', a_modulus)

                phase_minus = a_phase - angle
                # print('Phase minus:', phase_minus)

                a_minus_phase = rect(a_modulus, phase_minus)
                # print('A minus phase:', a_minus_phase)

                a_minus_phase_conjugate = a_minus_phase.conjugate()
                # print('A minus phase conjugate:', a_minus_phase_conjugate)

                a_minus_phase = phase(a_minus_phase_conjugate)
                a_minus_modulus = abs(a_minus_phase_conjugate)
                # print('A minus phase:', a_minus_phase)
                # print('A minus modulus:', a_minus_modulus)

                a_back_phase = a_minus_phase + angle
                # print('A back phase:', a_back_phase)

                d = rect(a_minus_modulus, a_back_phase)
                # print('D:', d)

                print(f'A:{a:25} B: {b:25} C:{c:25} D{d:25}')

            quit()

            for starting_cell in perimeter_coordinates[direction_name]:

                is_before_mirror = True
                paths[starting_cell]['before_mirror'] = set()
                paths[starting_cell]['after_mirror'] = set()
                q = [(starting_cell, starting_direction)]

                while q:
                    cell, direction = q.pop()

                    print('Cell:', cell)
                    print('Direction:', direction)
                    print('Value:', self.all_cells[cell])

                    if self.all_cells[cell] == '\\':
                        is_before_mirror = False
                        new_direction = direction * -1j

                    elif self.all_cells[cell] == '/':
                        is_before_mirror = False
                        new_direction = direction * 1j

                    else:
                        paths[starting_cell]['before_mirror' if is_before_mirror else 'after_mirror'] |= {cell}
                        new_direction = direction

                    new_cell = cell + new_direction

                    print('New direction:', new_direction)
                    print('New cell:', new_cell)
                    print()

                    if new_cell in self.all_cells:
                        q.append((new_cell, new_direction))

                quit()






def undead(house_plan: Tuple[str, ...],
           monsters: Dict[str, int],
           counts: Dict[str, List[int]]) -> Tuple[str, ...]:
    board = Board(house_plan, monsters, counts)

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
