from cmath import exp, pi
from collections import defaultdict
from copy import deepcopy
from typing import Tuple, Dict, List


class Board:
    EMPTY = '.'
    MIRRORS = '\\/'
    MONSTERS = 'VGZ'

    @staticmethod
    def round_complex(function):
        def function_with_rounding(*args, **kwargs):
            complex_result = function(*args, **kwargs)
            rounded_result = complex(int(complex_result.real), int(complex_result.imag))
            return rounded_result

        return function_with_rounding

    @staticmethod
    @round_complex.__get__(...)
    def mirror(vector, mirror_angle):

        rotated_minus_angle = vector * exp(1j * -mirror_angle)
        conjugated = rotated_minus_angle.conjugate()
        rotated_plus_angle = conjugated * exp(1j * mirror_angle)

        # rotated_minus_angle = vector * (cos(-mirror_angle) + 1j * sin(-mirror_angle))
        # conjugated = rotated_minus_angle.conjugate()
        # rotated_plus_angle = conjugated * (cos(mirror_angle) + 1j * sin(mirror_angle))
        #
        # rotated_minus_angle = rect(abs(vector), phase(vector) - mirror_angle)
        # conjugated = rotated_minus_angle.conjugate()
        # rotated_minus_angle = rect(abs(conjugated), phase(conjugated) + mirror_angle)

        # rounded = complex(int(rotated_plus_angle.real), int(rotated_plus_angle.imag))
        # return rounded

        return rotated_plus_angle

    def __init__(self, house_plan, target_monsters_per_path):
        plan = [row.replace(' ', '') for row in house_plan]
        [print(row) for row in plan]
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

        self.paths = self.calculate_paths()

        self.possible_monsters = {cell: set(self.MONSTERS) for cell in self.empty_cells}

        self.monsters = defaultdict(set)
        self.monsters_per_path = defaultdict(list)
        self.target_monsters_per_path = target_monsters_per_path
        self.is_monster_count_exceeded = False

        self.check_zeroes()

    @property
    def output(self):
        output_list = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                letter = self.plan[y][x]
                for monster_type in self.monsters:
                    if complex(y, x) in self.monsters[monster_type]:
                        letter = monster_type
                row += letter
            output_list.append(' '.join(list(row)))
        return output_list

    @property
    def monsters_counter(self):
        return {value: len(self.monsters[monster_type])
                for value, monster_type 
                in zip('vampire ghost zombie'.split(), self.MONSTERS)}

    def check_zeroes(self):

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                if self.target_monsters_per_path[direction][m_index] > 0:
                    continue

                for path_part in self.paths[direction][starting_cell]:
                    for cell in self.paths[direction][starting_cell][path_part]:
                        if path_part == 'before_mirror':
                            self.possible_monsters[cell] -= {'Z', 'V'}
                        if path_part == 'after_mirror':
                            self.possible_monsters[cell] -= {'Z', 'G'}


    def count_monsters_per_path(self):

        # self.monsters['Z'] |= {1 + 1j}

        monsters_per_path = defaultdict(list)

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                monster_count = 0
                for path_part in self.paths[direction][starting_cell]:

                    for cell in self.paths[direction][starting_cell][path_part]:
                        if cell in self.monsters['Z']:
                            monster_count += 1
                        if cell in self.monsters['V'] and path_part == 'before_mirror':
                            monster_count += 1
                        if cell in self.monsters['G'] and path_part == 'after_mirror':
                            monster_count += 1

                monster_count_target = self.target_monsters_per_path[direction][m_index]

                if monster_count > monster_count_target:
                    # print('---- Monster count exceeded:')
                    # print('Direction:', direction)
                    # print('Starting cell:', starting_cell)
                    # print('Self.monster_per_path[direction]:', self.monsters_per_path[direction])
                    # print('M index:', m_index)
                    # print('Monster count target:', monster_count_target)
                    # print('Monster count:', monster_count)
                    self.is_monster_count_exceeded = True
                    return

                monsters_per_path[direction].append(monster_count)

        self.monsters_per_path = monsters_per_path

    def calculate_paths(self):

        perimeter_coordinates = {'N': [complex(0, x) for x in range(self.width)],
                                 'W': [complex(y, 0) for y in range(self.height)],
                                 'S': [complex(self.height - 1, x) for x in range(self.width)],
                                 'E': [complex(y, self.width - 1) for y in range(self.height)]}

        paths = defaultdict(dict)

        for starting_direction, direction_name in zip((-1j, 1, -1, 1j), 'ENSW'):
            # print('Direction name starting direction:', direction_name, starting_direction)

            for starting_cell in perimeter_coordinates[direction_name]:

                is_before_mirror = True
                paths[direction_name][starting_cell] = {'before_mirror': set(), 'after_mirror': set()}
                q = [(starting_cell, starting_direction)]

                while q:
                    cell, direction = q.pop()

                    # print('Cell:', cell)
                    # print('Direction:', direction)
                    # print('Value:', self.all_cells[cell])

                    if self.all_cells[cell] == '\\':
                        is_before_mirror = False
                        new_direction = self.mirror(direction, pi / 4)

                    elif self.all_cells[cell] == '/':
                        is_before_mirror = False
                        new_direction = self.mirror(direction, -pi / 4)

                    else:
                        path_part = 'before_mirror' if is_before_mirror else 'after_mirror'
                        paths[direction_name][starting_cell][path_part] |= {cell}
                        new_direction = direction

                    new_cell = cell + new_direction

                    # print('New direction:', new_direction)
                    # print('New cell:', new_cell)
                    # print()

                    if new_cell in self.all_cells:
                        q.append((new_cell, new_direction))

        return paths


def undead(house_plan: Tuple[str, ...],
           monsters: Dict[str, int],
           counts: Dict[str, List[int]]) -> Tuple[str, ...]:

    board = Board(house_plan, counts)

    tick = 0
    q = [board]
    while q:
        board = q.pop()

        for cell in board.empty_cells:
            for monster_type in board.possible_monsters[cell]:
                print('Tick:', tick)
                tick += 1
                new_board = deepcopy(board)
                new_board.monsters[monster_type] |= {cell}
                new_board.empty_cells -= {cell}
                new_board.possible_monsters.pop(cell)
                new_board.count_monsters_per_path()

                [print(row) for row in new_board.output]
                print('New board monsters per path:', new_board.monsters_per_path)

                if new_board.is_monster_count_exceeded:
                    continue
                if new_board.monsters_per_path == new_board.target_monsters_per_path:
                    print('New board monsters counter:', new_board.monsters_counter)
                    print('Monsters:', monsters)
                    if new_board.monsters_counter != monsters:
                        continue
                    print('==== Matched')
                    print('New board output:', new_board.output)
                    return new_board.output

                q.append(new_board)

    raise ValueError


if __name__ == '__main__':
    TESTS = (
        # (
        #     ('. \\ . /',
        #      '\\ . . .',
        #      '/ \\ . \\',
        #      '. \\ / .'),
        #     {'ghost': 2, 'vampire': 2, 'zombie': 4},
        #     {'E': [0, 3, 0, 1],
        #      'N': [3, 0, 3, 0],
        #      'S': [2, 1, 1, 4],
        #      'W': [4, 0, 0, 0]},
        #     ('Z \\ V /',
        #      '\\ Z G V',
        #      '/ \\ Z \\',
        #      'G \\ / Z'),
        # ),
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
        # (
        #     ('. . . / . . /',
        #      '. . \\ / . . .',
        #      '. . . . . . .',
        #      '. \\ . . . / \\',
        #      '. / . \\ . . \\'),
        #     {'ghost': 6, 'vampire': 10, 'zombie': 9},
        #     {'E': [0, 4, 6, 0, 1],
        #      'N': [3, 5, 0, 3, 3, 7, 1],
        #      'S': [3, 0, 5, 0, 3, 0, 3],
        #      'W': [2, 4, 6, 0, 2]},
        #     ('Z Z G / V V /',
        #      'Z Z \\ / G V V',
        #      'G Z Z V Z Z V',
        #      'G \\ Z V V / \\',
        #      'V / V \\ G G \\'),
        # ),
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
