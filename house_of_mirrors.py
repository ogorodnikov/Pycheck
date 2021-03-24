from cmath import exp, pi
from collections import defaultdict, Counter
from copy import deepcopy
from heapq import heappop, heappush
from typing import Tuple, Dict, List


class Board:
    EMPTY = '.'
    MIRRORS = '\\/'
    MONSTERS = 'VGZ'

    @staticmethod
    def mirror(vector, mirror_angle):
        rotated_minus_angle = vector * exp(1j * -mirror_angle)
        conjugated = rotated_minus_angle.conjugate()
        rotated_plus_angle = conjugated * exp(1j * mirror_angle)
        rounded_result = complex(int(rotated_plus_angle.real),
                                 int(rotated_plus_angle.imag))
        return rounded_result

    def __init__(self, house_plan, target_monsters_per_path):
        plan = [row.replace(' ', '') for row in house_plan]
        self.plan = plan
        self.height = len(plan)
        self.width = len(plan[0])

        self.all_cells = {complex(y, x): plan[y][x]
                          for y in range(self.height)
                          for x in range(self.width)}

        self.room_cells = {cell for cell in self.all_cells
                           if self.all_cells[cell] in self.EMPTY}

        self.mirror_cells = {cell for cell in self.all_cells
                             if self.all_cells[cell] in self.MIRRORS}

        self.paths = self.calculate_paths()

        self.monsters = {cell: set(self.MONSTERS) for cell in self.room_cells}

        self.monsters_per_path = defaultdict(list)
        self.target_monsters_per_path = target_monsters_per_path
        self.is_monster_count_mismatched = False


    def copy(self):
        new_board = Board.__new__(Board)

        new_board.plan = self.plan
        new_board.height = self.height
        new_board.width = self.width

        new_board.all_cells = self.all_cells.copy()
        new_board.room_cells = self.room_cells.copy()
        new_board.mirror_cells = self.mirror_cells.copy()

        new_board.paths = {direction: {starting_cell: self.paths[direction][starting_cell].copy()
                                       for starting_cell in self.paths[direction]}
                           for direction in self.paths}

        new_board.monsters = {cell: monsters.copy() for cell, monsters in self.monsters.items()}

        new_board.monsters_per_path = self.monsters_per_path.copy()
        new_board.target_monsters_per_path = self.target_monsters_per_path.copy()
        new_board.is_monster_count_mismatched = self.is_monster_count_mismatched

        return new_board

    def set_monster(self, cell, monster_type):
        self.monsters[cell] = {monster_type}

    def remove_monster(self, cell, monster_type):
        self.monsters[cell] -= {monster_type}

    @property
    def undefined_cells(self):
        return {cell for cell, monsters in self.monsters.items() if len(monsters) > 1}

    @property
    def defined_cells(self):
        return {cell for cell, monsters in self.monsters.items() if len(monsters) == 1}

    @property
    def output(self):
        output_list = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                letter = self.plan[y][x]
                cell = complex(y, x)
                try:
                    monsters = self.monsters[cell]
                    if len(monsters) == 1:
                        letter = next(iter(monsters))
                except KeyError:
                    pass
                row += letter
            output_list.append(' '.join(list(row)))
        return output_list

    @property
    def monsters_counter(self):
        monsters_counts = Counter(next(iter(monster)) for cell, monster in self.monsters.items()
                                  if cell in self.defined_cells)
        return {value: monsters_counts[monster_type]
                for value, monster_type
                in zip('vampire ghost zombie'.split(), self.MONSTERS)}

    def check_maximum(self):

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                if self.paths[direction][starting_cell]['is_calculated']:
                    # print('---- Already calculated')
                    continue

                monster_count_target = self.target_monsters_per_path[direction][m_index]

                before_mirror = self.paths[direction][starting_cell]['before_mirror']
                after_mirror = self.paths[direction][starting_cell]['after_mirror']

                # visible_before_mirror = {cell for cell in before_mirror
                #                          if self.monsters[cell] in ({'Z'}, {'V'})}
                # visible_after_mirror = {cell for cell in after_mirror
                #                         if self.monsters[cell] in ({'Z'}, {'G'})}
                #
                # defined = {cell for cell in before_mirror | after_mirror
                #            if len(self.monsters[cell]) == 1}
                #
                # if len(before_mirror) - len(visible_before_mirror) + len(after_mirror) - len(visible_after_mirror) \
                #         == monster_count_target:
                #
                #     for cell in before_mirror - visible_before_mirror - defined:
                #         self.remove_monster(cell, 'G')
                #
                #     for cell in after_mirror - visible_after_mirror - defined:
                #         self.remove_monster(cell, 'V')

                new_visible_before_mirror = {cell for cell in before_mirror
                                             if self.monsters[cell] in ({'Z'}, {'V'}, {'Z', 'V'})}
                new_visible_after_mirror = {cell for cell in after_mirror
                                            if self.monsters[cell] in ({'Z'}, {'G'}, {'Z', 'G'})}

                invisible_before_mirror = {cell for cell in before_mirror
                                             if self.monsters[cell] == {'G'}}
                invisible_after_mirror = {cell for cell in after_mirror
                                            if self.monsters[cell] == {'V'}}

                if len(before_mirror) - len(invisible_before_mirror) + len(after_mirror) - len(invisible_after_mirror) \
                        == monster_count_target:

                    [print(row) for row in self.output]
                    print()
                    print('XXXX Fill visible:')
                    print('Direction:', direction)
                    print('Starting cell:', starting_cell)
                    print('    Before mirror:', [(cell, self.monsters[cell]) for cell in before_mirror], len(before_mirror))
                    print('    Invisible:', invisible_before_mirror, len(invisible_before_mirror))
                    print('    After mirror:', [(cell, self.monsters[cell]) for cell in after_mirror], len(after_mirror))
                    print('    Invisible:', invisible_after_mirror, len(invisible_after_mirror))
                    print()

                    for cell in before_mirror - invisible_before_mirror:
                        print('    Remove:', cell, 'G')
                        print('        Before:', self.monsters[cell])
                        self.remove_monster(cell, 'G')
                        print('        After:', self.monsters[cell])

                    for cell in after_mirror - invisible_after_mirror:
                        print('    Remove:', cell, 'V')
                        print('        Before:', self.monsters[cell])
                        self.remove_monster(cell, 'V')
                        print('        After:', self.monsters[cell])

                    input()

                if len(new_visible_before_mirror) + len(new_visible_after_mirror) == monster_count_target:

                    for cell in before_mirror - new_visible_before_mirror:
                        self.set_monster(cell, 'G')

                    for cell in after_mirror - new_visible_after_mirror:
                        self.set_monster(cell, 'V')



    def count_monsters_per_path(self):

        monsters_per_path = defaultdict(list)

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                if self.paths[direction][starting_cell]['is_calculated']:
                    old_monster_count = self.monsters_per_path[direction][m_index]
                    monsters_per_path[direction].append(old_monster_count)
                    continue

                full_path = set()
                monster_count = 0

                for cell in self.paths[direction][starting_cell]['before_mirror']:
                    if self.monsters[cell] in ({'Z'}, {'V'}):
                        monster_count += 1
                    full_path |= {cell}

                for cell in self.paths[direction][starting_cell]['after_mirror']:
                    if self.monsters[cell] in ({'Z'}, {'G'}):
                        monster_count += 1
                    full_path |= {cell}

                monster_count_target = self.target_monsters_per_path[direction][m_index]
                is_path_defined = full_path <= self.defined_cells

                if (monster_count > monster_count_target or
                        monster_count < monster_count_target and is_path_defined):
                    self.is_monster_count_mismatched = True
                    return

                if is_path_defined:
                    self.paths[direction][starting_cell]['is_calculated'] = True

                monsters_per_path[direction].append(monster_count)

        self.monsters_per_path = monsters_per_path

    def calculate_paths(self):

        perimeter_coordinates = {'N': [complex(0, x) for x in range(self.width)],
                                 'W': [complex(y, 0) for y in range(self.height)],
                                 'S': [complex(self.height - 1, x) for x in range(self.width)],
                                 'E': [complex(y, self.width - 1) for y in range(self.height)]}

        paths = defaultdict(dict)

        for starting_direction, direction_name in zip((-1j, 1, -1, 1j), 'ENSW'):

            for starting_cell in perimeter_coordinates[direction_name]:

                is_before_mirror = True
                paths[direction_name][starting_cell] = {'before_mirror': set(),
                                                        'after_mirror': set(),
                                                        'is_calculated': False}
                q = [(starting_cell, starting_direction)]

                while q:
                    cell, direction = q.pop()

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

                    if new_cell in self.all_cells:
                        q.append((new_cell, new_direction))

        return paths


def undead(house_plan: Tuple[str, ...],
           monsters: Dict[str, int],
           counts: Dict[str, List[int]]) -> Tuple[str, ...]:
    board = Board(house_plan, counts)

    tick = 0
    q = [(0, tick, board)]

    while q:
        *_, board = heappop(q)

        for cell in board.undefined_cells:
            for monster_type in board.monsters[cell]:

                if not tick % 10000 and tick > 0:
                    print('Tick:', tick)
                    [print(row) for row in new_board.output]
                    print('New board monsters per path:', new_board.monsters_per_path)
                    print()
                tick += 1

                new_board = board.copy()

                new_board.set_monster(cell, monster_type)
                new_board.check_maximum()
                new_board.count_monsters_per_path()

                if new_board.is_monster_count_mismatched:
                    continue
                if new_board.monsters_per_path == new_board.target_monsters_per_path:
                    print('New board monsters counter:', new_board.monsters_counter)
                    print('Monsters:', monsters)
                    if new_board.monsters_counter != monsters:
                        continue
                    print('==== Matched')
                    print('Tick:', tick)
                    print('New board output:', new_board.output)
                    return new_board.output

                priority = -len(new_board.defined_cells)
                # priority = sum(len(new_board.monsters[cell]) for cell in new_board.room_cells)

                heappush(q, (priority, tick, new_board))

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
        # (
        #     ('\\ . . .',
        #      '. . \\ /',
        #      '/ \\ . \\',
        #      '/ . \\ \\',
        #      '. . . .',
        #      '/ / . /'),
        #     {'ghost': 3, 'vampire': 5, 'zombie': 4},
        #     {'E': [1, 0, 0, 3, 4, 0],
        #      'N': [2, 1, 2, 0],
        #      'S': [0, 3, 3, 0],
        #      'W': [0, 3, 0, 0, 4, 2]},
        #     ('\\ G V G',
        #      'V G \\ /',
        #      '/ \\ Z \\',
        #      '/ V \\ \\',
        #      'Z V Z Z',
        #      '/ / V /'),
        # ),
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
