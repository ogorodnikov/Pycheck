from collections import namedtuple

NEIGHBOURS_9 = ((-1, -1), (0, -1), (1, -1),  # 0 1 2
                (-1, 0), (0, 0), (1, 0),  # 3 4 5
                (-1, 1), (0, 1), (1, 1))  # 6 7 8

NEIGHBOURS_CORNERS = ((-1, -1), (1, -1),  # 0 2
                      (-1, 1), (1, 1))  # 6 8

MIN_BACTERIA_LEVEL = 1
OUT_OF_BORDER_CELL_VALUE = 0
PATTERN_WIDTH = 3

PATTERN_MODEL = ('00001000000000100000000010000',
                 '00011100000001110000000111000',
                 '00101010000011111000001111100',
                 '01110111000101110100011111110',
                 '00101010001110101110001111100',
                 '00011100011111011111000111000',
                 '00001000001110101110000010000',
                 '00000000000101110100000000000',
                 '00000000000011111000000000000',
                 '00000000000001110000000000000',
                 '00000000000000100000000000000')


def parse_pattern_model(pattern_model):
    map_height = len(pattern_model)
    map_width = len(pattern_model[0])
    border_patterns = set()
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
            border_patterns.add(pattern_string_list)

    # print_map('Pacing pattern model:', pattern_model)
    # print('Parsed border patterns:')
    # for i, border_pattern_lines in enumerate(border_patterns):
    #     print(f'{i})')
    #     for border_pattern_line in border_pattern_lines:
    #         print(border_pattern_line)
    #     print()
    # print('Border patterns parsed:', len(border_patterns))
    # print()
    return border_patterns


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


def find_healthy_colonies(grid, border_patterns):
    checked = []
    colonies = []
    colonies_pattern_strings = []
    map_height = len(grid)
    map_width = len(grid[0])
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value < MIN_BACTERIA_LEVEL:
                continue
            if (x, y) in checked:
                continue
            # traverse colony
            q = [((x, y), value)]
            checked.append((x, y))
            colony_cells = [(x, y)]
            is_healthy_colony = True
            colony_pattern_strings = []
            while q:
                a, a_value = q.pop()
                ax, ay = a
                a_pattern_string = ''
                for dx, dy in NEIGHBOURS_9:
                    bx, by = ax + dx, ay + dy
                    if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                        a_pattern_string += str(OUT_OF_BORDER_CELL_VALUE)
                        continue
                    b = bx, by
                    b_value = grid[by][bx]
                    if b_value == a_value:
                        a_pattern_string += str(MIN_BACTERIA_LEVEL)
                    else:
                        a_pattern_string += str(OUT_OF_BORDER_CELL_VALUE)
                    if (dx, dy) in NEIGHBOURS_CORNERS:
                        continue
                    if b in checked or b_value < MIN_BACTERIA_LEVEL:
                        continue
                    q.append((b, b_value))
                    checked.append(b)
                    colony_cells.append(b)
                pattern_string_list = tuple(a_pattern_string[i:i + PATTERN_WIDTH]
                                            for i in range(0, PATTERN_WIDTH * PATTERN_WIDTH, PATTERN_WIDTH))
                in_border_patterns = pattern_string_list in border_patterns
                if not in_border_patterns:
                    is_healthy_colony = False
                colony_pattern_strings.append((a, a_pattern_string, pattern_string_list, in_border_patterns))

            print('Found colony:', *sorted(colony_cells))
            print_colony(colony_cells)
            print('Is healthy:', is_healthy_colony)
            if is_healthy_colony:
                min_x, min_y = min(colony_cells)
                max_x, max_y = max(colony_cells)
                diameter = max_x - min_x
                center_x = min_x + diameter // 2
                center_y = min_y
                center = center_x, center_y

                Colony = namedtuple('Colony', ['cells', 'center', 'diameter'])
                current_colony = Colony(colony_cells, center, diameter)
                colonies.append(current_colony)

            print('Adding colony pattern strings:')
            for colony_pattern_string in sorted(colony_pattern_strings):
                print(colony_pattern_string)
            colonies_pattern_strings.append(colony_pattern_strings)
            print()

    return colonies


def healthy(grid):
    print_map('Grid', grid)
    print()
    border_patterns = parse_pattern_model(PATTERN_MODEL)
    healthy_colonies = find_healthy_colonies(grid, border_patterns)
    print('Healthy colonies:')
    for healthy_colony in healthy_colonies:
        print(healthy_colony)
    if healthy_colonies:
        largest_healthy_colony = max(healthy_colonies, key=lambda colony: colony.diameter)
        largest_healthy_colony_center = largest_healthy_colony.center
    else:
        largest_healthy_colony_center = (0, 0)
    print('Largest healthy colony center:', largest_healthy_colony_center)
    print()
    return reversed(largest_healthy_colony_center)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def check(result, answers):
        return list(result) in answers

    assert check(healthy(((0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0),
                          (0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0), (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0),
                          (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0), (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
                          (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                          (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0), (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
                          (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0),
                          (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0), (0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0),
                          (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0))), [[7, 7]])

    assert check(healthy(((0, 1, 0),
                          (1, 1, 1),
                          (0, 1, 0),)), [[1, 1]])

    assert check(healthy(((0, 0, 1, 0, 0),
                          (0, 1, 1, 1, 0),
                          (0, 0, 1, 0, 0),
                          (0, 0, 0, 0, 0),
                          (0, 0, 1, 0, 0),)), [[1, 2]])

    assert check(healthy(((0, 0, 1, 0, 0),
                          (0, 1, 1, 1, 0),
                          (0, 0, 1, 0, 0),
                          (0, 0, 1, 0, 0),
                          (0, 0, 1, 0, 0),)), [[0, 0]])

    assert check(healthy(((0, 0, 0, 0, 0, 0, 0, 0),
                          (0, 0, 1, 0, 0, 0, 0, 0),
                          (0, 1, 1, 1, 0, 0, 0, 0),
                          (1, 1, 1, 1, 1, 0, 0, 0),
                          (0, 1, 1, 1, 0, 0, 0, 0),
                          (0, 0, 1, 0, 0, 0, 0, 0),
                          (0, 0, 0, 0, 0, 0, 0, 0),)), [[3, 2]])

    assert check(healthy(((0, 0, 0, 0, 0, 0, 1, 0),
                          (0, 0, 1, 0, 0, 1, 1, 1),
                          (0, 1, 1, 1, 0, 0, 1, 0),
                          (1, 1, 1, 1, 1, 0, 0, 0),
                          (0, 1, 1, 1, 0, 0, 1, 0),
                          (0, 0, 1, 0, 0, 1, 1, 1),
                          (0, 0, 0, 0, 0, 0, 1, 0),)), [[3, 2]])

    assert check(healthy(((0, 0, 0, 0, 0, 0, 2, 0),
                          (0, 0, 0, 2, 2, 2, 2, 2),
                          (0, 0, 1, 0, 0, 0, 2, 0),
                          (0, 1, 1, 1, 0, 0, 2, 0),
                          (1, 1, 1, 1, 1, 0, 2, 0),
                          (0, 1, 1, 1, 0, 0, 2, 0),
                          (0, 0, 1, 0, 0, 0, 2, 0),
                          (0, 0, 0, 1, 0, 0, 2, 0),
                          (0, 0, 1, 1, 1, 0, 2, 0),
                          (0, 1, 1, 1, 1, 1, 0, 0),
                          (0, 0, 1, 1, 1, 0, 0, 0),
                          (0, 0, 0, 1, 0, 0, 0, 0),)), [[4, 2], [9, 3]])

