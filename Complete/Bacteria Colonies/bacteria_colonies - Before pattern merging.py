NEIGHBOURS_9 = (-1, -1), (0, -1), (1, -1),\
               (-1,  0), (0,  0), (1,  0), \
               (-1,  1), (0,  1), (1,  1)
MIN_BACTERIA_LEVEL = 1

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


def in_patterns(a, grid):
    ax, ay = a
    for dy, dx in NEIGHBOURS_8:
        bx, by = ax + dx, ay + dy
        b = bx, by
        print(b)


def print_path(path):
    signs = dict()
    signs[path[-1]] = 'X'
    for step, next_step in zip(path, path[1:]):
        step_x, step_y = step
        next_step_x, next_step_y = next_step
        if next_step_x > step_x:
            sign = '>'
        elif next_step_x < step_x:
            sign = '<'
        elif next_step_y > step_y:
            sign = 'Y'
        elif next_step_y < step_y:
            sign = '^'
        else:
            sign = '?'
        signs[step] = sign

    # print('Signs:')
    # for sign in signs.items():
    #     print(*sign)

    path_height = max(y for x, y in path) + 1
    path_width = max(x for x, y in path) + 1
    row_number_width = (path_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(path_width))

    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(path_height):
        row_number_width = (path_height - 1) // 10 + 1
        print(f'{y:{row_number_width}d}', end=' ')
        for x in range(path_width):
            cell_value = signs[(x, y)] if (x, y) in signs else ' '
            print(cell_value, end='')
        print('\r')


def is_isolated(ax, ay, elevation_map):
    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    for dy, dx in NEIGHBOURS_4:
        bx, by = ax + dx, ay + dy
        if map_width <= bx or bx < 0 or map_height <= by or by < 0:
            continue
        b_value = int(elevation_map[by][bx])
        if b_value >= MIN_MOUNTAIN_HEIGHT:
            return False
    return True


def find_healthy_colonies(grid):
    checked = []
    colonies = []
    map_height = len(grid)
    map_width = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell < MIN_BACTERIA_LEVEL:
                continue
            if (x, y) in checked:
                continue
            # traverse colony
            colony_cells = set()
            q = [(x, y)]
            while q:
                a = q.pop()
                checked.append(a)
                colony_cells.add(a)
                ax, ay = a
                for dy, dx in NEIGHBOURS_9:
                    bx, by = ax + dx, ay + dy
                    if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                        continue
                    b = bx, by
                    b_value = grid[by][bx]
                    if b in checked or b_value < MIN_BACTERIA_LEVEL:
                        continue
                    q.append(b)
            print('Adding colony:', *sorted(colony_cells))
            colonies.append(colony_cells)

            for colony_cells in colonies:
                colony_patterns = []
                for a in colony_cells:
                    print('A:', a)
                    b_pattern = ''
                    ax, ay = a
                    for dx, dy in NEIGHBOURS_9:
                        bx, by = ax + dx, ay + dy
                        if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                            b_value = 0
                        else:
                            b_value = grid[by][bx]
                        b_pattern += str(b_value)
                    b_pattern_list = [b_pattern[i:i+3] for i in range(0, 9, 3)]
                    print_map('B pattern list:', b_pattern_list)
                    colony_patterns.append(b_pattern_list)

                print()
                print('Colony patterns:')
                for colony_pattern in colony_patterns:
                    print(colony_pattern)
                    print(tuple(colony_pattern) in BORDER_PATTERNS)
                print('All colony patterns in border patterns?')
                print(all(tuple(colony_pattern) in BORDER_PATTERNS for colony_pattern in colony_patterns))

                print()
                print('Border patterns:')
                for border_pattern in BORDER_PATTERNS:
                    print(border_pattern)





def healthy(grid):
    print_map('Map', grid)
    print()
    find_healthy_colonies(grid)
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
