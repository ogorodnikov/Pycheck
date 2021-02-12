NEIGHBOURS_9 = ((-1, -1), (0, -1), (1, -1),  # 0 1 2
                (-1, 0), (0, 0), (1, 0),     # 3 4 5
                (-1, 1), (0, 1), (1, 1))     # 6 7 8
MIN_BACTERIA_LEVEL = 1
OUT_OF_BORDER_CELL_VALUE = 0
PATTERN_WIDTH = 3

PATTERN_MODEL = ('001000000',
                 '011100000',
                 '111110010',
                 '011100111',
                 '001000010')

BORDER_PATTERNS = (('000',
                    '010',
                    '111'),
                   ('100',
                    '110',
                    '100'),
                   ('111',
                    '010',
                    '000'),
                   ('001',
                    '011',
                    '001'),

                   ('001',
                    '011',
                    '111'),
                   ('100',
                    '110',
                    '111'),
                   ('111',
                    '110',
                    '100'),
                   ('111',
                    '011',
                    '001'),

                   ('010',
                    '111',
                    '010'),

                   ('010',
                    '111',
                    '111'),
                   ('110',
                    '111',
                    '110'),
                   ('111',
                    '111',
                    '010'),
                   ('011',
                    '111',
                    '011'),

                   ('111',
                    '111',
                    '111'))


def parse_pattern_model(pattern_model):
    map_height = len(pattern_model)
    map_width = len(pattern_model[0])
    border_patterns = []

    print_map('Pacing pattern model:', pattern_model)
    print('Height:', map_height)
    print('Width:', map_width)

    for ay in range(map_height):
        for ax in range(map_width):
            cell_a = pattern_model[ay][ax]
            if int(cell_a) < MIN_BACTERIA_LEVEL:
                continue
            a_pattern_string = ''
            for dx, dy in NEIGHBOURS_9:
                bx, by = ax + dx, ay + dy
                if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                    a_pattern_string += str(OUT_OF_BORDER_CELL_VALUE)
                    continue
                b_value = pattern_model[by][bx]
                a_pattern_string += str(b_value)
            pattern_string_list = tuple(a_pattern_string[i:i + PATTERN_WIDTH]
                                        for i in range(0, PATTERN_WIDTH * PATTERN_WIDTH, PATTERN_WIDTH))
            border_patterns.append(pattern_string_list)
    print('Parsed border patterns:')
    for i, border_pattern_lines in enumerate(border_patterns):
        print(f'{i})')
        for border_pattern_line in border_pattern_lines:
            print(border_pattern_line)
        print()

    print('Length of parsed patterns:', len(border_patterns))


    border_patterns_set = set(border_patterns)
    print('Parsed border patterns set:')
    for i, border_pattern_lines in enumerate(border_patterns_set):
        print(f'{i})', border_pattern_lines, border_pattern_lines in BORDER_PATTERNS)
        for border_pattern_line in border_pattern_lines:
            print(border_pattern_line)
        print()

    print('Length of parsed patterns set:', len(border_patterns_set))

    print('Border patterns:')
    for i, border_pattern_lines in enumerate(BORDER_PATTERNS):
        print(f'{i})', border_pattern_lines, border_pattern_lines in border_patterns_set)
        for border_pattern_line in border_pattern_lines:
            print(border_pattern_line)
        print()

    print('Length of BORDER_PATTERNS:', len(BORDER_PATTERNS))


def print_map(caption, regional_map):
    if isinstance(regional_map[0], tuple):
        regional_map = [''.join(map(str, row)) for row in regional_map]
    map_height = len(regional_map)
    map_width = len(regional_map[0])
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print(caption)
    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y, row in enumerate(regional_map):
        print(f'{y:{row_number_width}d} {row}')


def print_colony(cells):
    map_height = max(y for x, y in cells) + 1
    map_width = max(x for x, y in cells) + 1
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(map_height):
        print(f'{y:{row_number_width}d} ', end='')
        for x in range(map_width):
            if (x, y) in cells:
                cell_value = 'X'
            else:
                cell_value = ' '
            print(cell_value, end='')
        print('\r')


def find_healthy_colonies(grid):
    checked = []
    colonies = []
    colonies_pattern_strings = []
    map_height = len(grid)
    map_width = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell < MIN_BACTERIA_LEVEL:
                continue
            if (x, y) in checked:
                continue
            # traverse colony
            q = [(x, y)]
            checked.append((x, y))
            colony_cells = [(x, y)]
            is_healthy_colony = True
            colony_pattern_strings = []
            while q:
                a = q.pop()
                ax, ay = a
                a_pattern_string = ''
                for dx, dy in NEIGHBOURS_9:
                    bx, by = ax + dx, ay + dy
                    if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                        a_pattern_string += str(OUT_OF_BORDER_CELL_VALUE)
                        continue
                    b = bx, by
                    b_value = grid[by][bx]
                    a_pattern_string += str(b_value)
                    if b in checked or b_value < MIN_BACTERIA_LEVEL:
                        continue
                    q.append(b)
                    checked.append(b)
                    colony_cells.append(b)
                pattern_string_list = tuple(a_pattern_string[i:i + PATTERN_WIDTH]
                                            for i in range(0, PATTERN_WIDTH * PATTERN_WIDTH, PATTERN_WIDTH))
                in_border_patterns = pattern_string_list in BORDER_PATTERNS
                if not in_border_patterns:
                    is_healthy_colony = False
                colony_pattern_strings.append((a, a_pattern_string, pattern_string_list, in_border_patterns))

            print('Adding colony:', *sorted(colony_cells))
            print_colony(colony_cells)
            colonies.append(colony_cells)
            print('Is healthy:', is_healthy_colony)
            print('Checked:', checked)

            print('Adding colony pattern strings:')
            for colony_pattern_string in sorted(colony_pattern_strings):
                print(colony_pattern_string)
            colonies_pattern_strings.append(colony_pattern_strings)
            print('Border patterns:')
            for border_pattern in BORDER_PATTERNS:
                print(border_pattern)
            print()


def healthy(grid):
    print_map('Map', grid)
    print()
    find_healthy_colonies(grid)
    parse_pattern_model(PATTERN_MODEL)
    return 1, 1


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def check(result, answers):
        return list(result) in answers


    assert check(healthy(((0, 1, 0),
                          (1, 1, 1),
                          (0, 1, 0),)), [[1, 1]])

    # check(healthy(((0, 0, 1, 0, 0),
    #                (0, 1, 1, 1, 0),
    #                (0, 0, 1, 0, 0),
    #                (0, 0, 0, 0, 0),
    #                (0, 0, 1, 0, 0),)), [[1, 2]])

    # check(healthy(((0, 0, 1, 0, 0),
    #                (0, 1, 1, 1, 0),
    #                (0, 0, 1, 0, 0),
    #                (0, 0, 1, 0, 0),
    #                (0, 0, 1, 0, 0),)), [[0, 0]])

    check(healthy(((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 1, 0, 0, 0, 0, 0),
                   (0, 1, 1, 1, 0, 0, 0, 0),
                   (1, 1, 1, 1, 1, 0, 0, 0),
                   (0, 1, 1, 1, 0, 0, 0, 0),
                   (0, 0, 1, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),)), [[3, 2]])

    # check(healthy(((0, 0, 0, 0, 0, 0, 1, 0),
    #                (0, 0, 1, 0, 0, 1, 1, 1),
    #                (0, 1, 1, 1, 0, 0, 1, 0),
    #                (1, 1, 1, 1, 1, 0, 0, 0),
    #                (0, 1, 1, 1, 0, 0, 1, 0),
    #                (0, 0, 1, 0, 0, 1, 1, 1),
    #                (0, 0, 0, 0, 0, 0, 1, 0),)), [[3, 2]])

    # check(healthy(((0, 0, 0, 0, 0, 0, 2, 0),
    #                (0, 0, 0, 2, 2, 2, 2, 2),
    #                (0, 0, 1, 0, 0, 0, 2, 0),
    #                (0, 1, 1, 1, 0, 0, 2, 0),
    #                (1, 1, 1, 1, 1, 0, 2, 0),
    #                (0, 1, 1, 1, 0, 0, 2, 0),
    #                (0, 0, 1, 0, 0, 0, 2, 0),
    #                (0, 0, 0, 1, 0, 0, 2, 0),
    #                (0, 0, 1, 1, 1, 0, 2, 0),
    #                (0, 1, 1, 1, 1, 1, 0, 0),
    #                (0, 0, 1, 1, 1, 0, 0, 0),
    #                (0, 0, 0, 1, 0, 0, 0, 0),)), [[4, 2], [9, 3]])
