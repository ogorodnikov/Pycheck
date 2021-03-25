from cmath import exp, pi
from collections import defaultdict, Counter
from heapq import heappop, heappush


class Board:
    EMPTY = '.'
    MIRRORS = '\\/'
    MONSTER_TYPES = 'ZVG'
    INPUT_MONSTER_TYPES = 'zombie', 'vampire', 'ghost'

    @staticmethod
    def mirror(vector, mirror_angle):
        rotated_minus_angle = vector * exp(1j * -mirror_angle)
        conjugated = rotated_minus_angle.conjugate()
        rotated_plus_angle = conjugated * exp(1j * mirror_angle)
        rounded_result = complex(int(rotated_plus_angle.real),
                                 int(rotated_plus_angle.imag))
        return rounded_result

    def __init__(self, house_plan, input_monsters, target_monsters_per_path):
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

        self.monsters = {cell: set(self.MONSTER_TYPES) for cell in self.room_cells}

        self.monsters_per_path = {'E': [0] * self.height, 'W': [0] * self.height,
                                  'S': [0] * self.width, 'N': [0] * self.width}

        self.target_monsters_per_path = target_monsters_per_path

        self.monster_counter_target = {monster_type: input_monsters[input_monster_type]
                                       for monster_type, input_monster_type
                                       in zip(self.MONSTER_TYPES, self.INPUT_MONSTER_TYPES)}

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
        new_board.monster_counter_target = self.monster_counter_target
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
    def hash(self):
        return hash(tuple(hash((hash(k), hash(tuple(v))))
                          for k, v in self.monsters.items()))

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
    def monster_counter(self):
        return Counter(next(iter(monster)) for cell, monster in self.monsters.items()
                       if cell in self.defined_cells)

    def check_monster_counts(self):

        monster_counter = self.monster_counter

        for monster_type in self.MONSTER_TYPES:
            if monster_counter[monster_type] > self.monster_counter_target[monster_type]:
                # print('>>>> Monster count exceeded')
                self.is_monster_count_mismatched = True
                return

            if monster_counter[monster_type] == self.monster_counter_target[monster_type]:
                for cell in self.undefined_cells:
                    # [print(row) for row in self.output]
                    # print('Cell:', cell)
                    # print('Monster type:', monster_type)
                    # print('Before:', self.monsters[cell])
                    self.remove_monster(cell, monster_type)
                    # print('After:', self.monsters[cell])
                    # input()

    def calculate_paths(self):

        perimeter_coordinates = {'N': [complex(0, x) for x in range(self.width)],
                                 'W': [complex(y, 0) for y in range(self.height)],
                                 'S': [complex(self.height - 1, x) for x in range(self.width)],
                                 'E': [complex(y, self.width - 1) for y in range(self.height)]}

        paths = defaultdict(dict)

        for starting_direction, direction_name in zip((-1j, 1, -1, 1j), 'ENSW'):

            for starting_cell in perimeter_coordinates[direction_name]:

                is_before_mirror = True
                paths[direction_name][starting_cell] = {'before_mirror': list(),
                                                        'after_mirror': list(),
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
                        paths[direction_name][starting_cell][path_part].append(cell)
                        new_direction = direction

                    new_cell = cell + new_direction

                    if new_cell in self.all_cells:
                        q.append((new_cell, new_direction))
        return paths

    def count_monsters_per_path(self):

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                if self.paths[direction][starting_cell]['is_calculated']:
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

                self.monsters_per_path[direction][m_index] = monster_count

    def check_maximum(self):

        for direction in self.paths:
            for m_index, starting_cell in enumerate(self.paths[direction]):

                if self.paths[direction][starting_cell]['is_calculated']:
                    continue

                before_mirror = self.paths[direction][starting_cell]['before_mirror']
                after_mirror = self.paths[direction][starting_cell]['after_mirror']

                visible_before_mirror = [cell for cell in before_mirror
                                         if self.monsters[cell] in ({'Z'}, {'V'}, {'Z', 'V'})]
                visible_after_mirror = [cell for cell in after_mirror
                                        if self.monsters[cell] in ({'Z'}, {'G'}, {'Z', 'G'})]

                invisible_before_mirror = [cell for cell in before_mirror
                                           if self.monsters[cell] == {'G'}]
                invisible_after_mirror = [cell for cell in after_mirror
                                          if self.monsters[cell] == {'V'}]

                monster_count_target = self.target_monsters_per_path[direction][m_index]

                if len(before_mirror) - len(invisible_before_mirror) + len(after_mirror) - len(invisible_after_mirror) \
                        == monster_count_target:

                    for cell in before_mirror:
                        if cell not in invisible_before_mirror:
                            self.remove_monster(cell, 'G')

                    for cell in after_mirror:
                        if cell not in invisible_after_mirror:
                            self.remove_monster(cell, 'V')

                if len(visible_before_mirror) + len(visible_after_mirror) == monster_count_target:

                    for cell in before_mirror:
                        if cell not in visible_before_mirror:
                            self.set_monster(cell, 'G')

                    for cell in after_mirror:
                        if cell not in visible_after_mirror:
                            self.set_monster(cell, 'V')

                if starting_cell == (6 + 5j):
                    [print(row) for row in self.output]
                    print('Direction:', direction)
                    print('Starting cell:', starting_cell)
                    print('Before mirror:', before_mirror)
                    print('After mirror:', after_mirror)
                    print('Before monsters:', [(cell, self.monsters[cell]) for cell in before_mirror])
                    print('After monsters:', [(cell, self.monsters[cell]) for cell in after_mirror])
                    quit()


def undead(house_plan, monsters, counts):
    board = Board(house_plan, monsters, counts)

    tick = 0
    hashes = []
    q = [(0, tick, board)]

    while q:
        *_, board = heappop(q)

        board.check_maximum()
        board.check_monster_counts()
        board.count_monsters_per_path()

        # [print(row) for row in board.output]
        # print('Monsters per path:', board.monsters_per_path)
        # print('Monsters:', board.monster_counter)
        # print('Target:  ', board.monster_counter_target)
        # print()
        # quit()

        # if board.output == ['Z Z \\ V V / V',
        #                     'Z G Z Z \\ V /',
        #                     'Z Z \\ \\ / / Z',
        #                     'Z V \\ \\ / V /',
        #                     '/ \\ G G G \\ \\',
        #                     '\\ Z V V G \\ V',
        #                     'V G \\ V G V \\']:
        #     [print(row) for row in board.output]
        #     print('>>>> Detected')

        if board.is_monster_count_mismatched:
            continue

        if board.monsters_per_path == board.target_monsters_per_path \
                and board.monster_counter == board.monster_counter_target:
            print('==== Matched')
            print('Tick:', tick)
            print('New board output:', board.output)
            return board.output

        monster_hash = board.hash
        if monster_hash in hashes:
            # print('---- Hash already there')
            continue
        hashes.append(monster_hash)

        for cell in board.undefined_cells:
            for monster_type in board.monsters[cell]:
                tick += 1

                new_board = board.copy()
                new_board.set_monster(cell, monster_type)

                if not tick % 10000:
                    print('Tick:', tick)
                    [print(row) for row in new_board.output]
                    print('Monsters per path:', new_board.monsters_per_path)
                    print('Monsters:', new_board.monster_counter)
                    print('Target:  ', new_board.monster_counter_target)
                    print()

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
        # (
        #     ["\\ . . .", ". / \\ .", "/ \\ . \\", ". . \\ /"],
        #     {"ghost": 5, "vampire": 1, "zombie": 2},
        #     {"N": [3, 0, 1, 0], "S": [2, 2, 2, 0], "W": [0, 2, 0, 2], "E": [0, 1, 2, 0]},
        #     ('\\ G G G', 'V / \\ G', '/ \\ G \\', 'Z Z \\ /'),
        # ),
        # (
        #     (". / . \\",
        #      "/ . / .",
        #      "\\ . \\ /",
        #      ". . \\ /",
        #      ". . . .",
        #      ". / . .",
        #      ". / . /"),
        #     {"ghost": 2, "vampire": 9, "zombie": 5},
        #     {"N": [1, 0, 1, 0],
        #      "S": [3, 0, 4, 0],
        #      "W": [1, 0, 3, 2, 4, 5, 2],
        #      "E": [0, 5, 1, 0, 4, 2, 0]},
        #     ("V / Z \\",
        #      "/ V / Z",
        #      "\\ V \\ /",
        #      "G Z \\ /",
        #      "V V V V",
        #      "Z / G V",
        #      "Z / V /"),
        # ),

        # (
        #     [". . \\ . . / .", ". . . . \\ . /", ". . \\ \\ / / .", ". . \\ \\ / . /", "/ \\ . . . \\ \\",
        #      "\\ . . . . \\ .", ". . \\ . . . \\"],
        #     {"ghost": 7, "vampire": 12, "zombie": 10},
        #     {"N": [4, 6, 0, 6, 1, 0, 1], "S": [1, 3, 1, 4, 1, 5, 3],
        #      "W": [3, 4, 3, 4, 4, 0, 1], "E": [4, 4, 1, 0, 0, 7, 1]},
        #     ('Z Z \\ V V / V',
        #      'Z G Z Z \\ V /',
        #      'Z Z \\ \\ / / Z',
        #      'Z V \\ \\ / V /',
        #      '/ \\ G G G \\ \\',
        #      '\\ Z V V G \\ V',
        #      'V G \\ V G V \\'),
        # ),

        (
            [". . . . . . .", ". . . \\ . \\ /", ". . . . . / \\", ". . . . / \\ \\", ". \\ \\ . \\ / .",
             "\\ . . . \\ / \\", ". \\ . . . . /"],
            {"ghost": 13, "vampire": 16, "zombie": 2},
            {"N": [4, 0, 4, 4, 4, 0, 2], "S": [0, 1, 6, 5, 5, 1, 0], "W": [4, 3, 4, 5, 1, 1, 0],
             "E": [4, 0, 0, 0, 1, 0, 0]},
            ('V G V G Z G V', 'G G V \\ G \\ /', 'G G V V G / \\', 'Z G V G / \\ \\', 'V \\ \\ V \\ / V',
             '\\ V V G \\ / \\', 'G \\ V V V V /')
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
