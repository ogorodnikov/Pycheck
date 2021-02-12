from heapq import heappop, heappush
from itertools import permutations, chain

NEIGHBOURS_4 = (1, 0), (0, 1), (-1, 0), (0, -1)
MAX_ELEVATION_STEP = 1


def print_map(caption, regional_map):
    print(caption)
    print('=' * 20)
    print(' ' * ((len(regional_map) - 1) // 10 + 2) + ''.join(str(i % 10) for i in range(len(regional_map[0]))))
    for y, row in enumerate(regional_map):
        print(f'{y:{(len(regional_map) - 1) // 10 + 1}d}', end=' ')
        for x, cell in enumerate(row):
            print(regional_map[y][x], end='')
        print('\r')


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


def find_tops(elevation_map):
    tops = []
    # islands = []
    checked = []
    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    for y, row in enumerate(elevation_map):
        for x, cell in enumerate(row):
            cell_value = int(cell)
            if cell_value > 0 and (x, y) not in checked:
                # traverse island
                top_cell = (x, y)
                top_value = cell_value
                # island_cells = []
                q = [(x, y)]
                while q:
                    a = q.pop()
                    checked.append(a)
                    # island_cells.append(a)
                    ax, ay = a
                    for dy, dx in NEIGHBOURS_4:
                        bx, by = ax + dx, ay + dy
                        if 0 <= bx < map_width and 0 <= by < map_height:
                            b = bx, by
                            b_value = int(elevation_map[by][bx])
                            if b_value > 0 and b not in checked:
                                q.append(b)
                                if b_value > top_value:
                                    top_cell = b
                                    top_value = b_value
                # yield island_cells
                # yield top_value
                yield top_cell


def get_distance(start, end, elevation_map):
    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    tick = 0
    q = [(0, tick, start, [start], 0)]
    while q:
        priority, _, a, path, path_len = heappop(q)
        if a == end:
            return path, path_len
        for dy, dx in NEIGHBOURS_4:
            ax, ay = a
            bx, by = ax + dx, ay + dy
            b = bx, by
            if b in path:
                continue
            if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                continue
            a_value = int(elevation_map[ay][ax])
            b_value = int(elevation_map[by][bx])
            if abs(b_value - a_value) > MAX_ELEVATION_STEP:
                continue
            end_x, end_y = end
            manhattan_distance = abs(end_x - bx) + abs(end_y - by)
            priority = manhattan_distance
            tick += 1
            heappush(q, (priority, id, b, path + [b], path_len + 1))


def climbing_route(elevation_map):
    print_map('Map:', elevation_map)

    for top_cell in find_tops(elevation_map):
        print('Top cell:', top_cell)
    print()

    # path, path_len = get_distance((0, 1), (2, 2), elevation_map)
    # print('Distance:', path_len)
    # print()
    # print_path('Path:', path)



    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    start = [(0, 0)]
    end = [(map_width - 1, map_height - 1)]

    total_distances = []
    for permutation in permutations(find_tops(elevation_map)):
        pairs = zip(chain(start, permutation), chain(permutation, end))

        print('Variant:')
        total_distance = 0
        for pair in pairs:
            print('Pair:', *pair)
            a, b = pair
            path, distance = get_distance(a, b, elevation_map)
            print_path(path)
            print('Distance:', distance)
            print()
            total_distance += distance

        total_distances.append(total_distance)
        print('Total distance:', total_distance)
        print()

    print('Total distances:', total_distances)
    min_total_distance = min(total_distances)
    print('Minimum total distance:', min_total_distance)
    print()
    return min_total_distance


if __name__ == '__main__':

    assert climbing_route([
        '000',
        '210',
        '000']) == 6, 'basic'

    assert climbing_route([
        '00000',
        '05670',
        '04980',
        '03210',
        '00000']) == 26, 'spiral'

    assert climbing_route([
        '000000001',
        '222322222',
        '100000000']) == 26, 'bridge'

    assert climbing_route([
        '000000120000',
        '001002432100',
        '012111211000',
        '001000000000']) == 16, 'one top'

    # assert climbing_route([
    #     '000000002110',
    #     '011100002310',
    #     '012100002220',
    #     '011100000000']) == 26, 'two top'
    # assert climbing_route([
    #     '00000000111111100',
    #     '00000000122222100',
    #     '00000000123332100',
    #     '00000000123432100',
    #     '00000000123332100',
    #     '00000000122222100',
    #     '00000000111111100',
    #     '00011111000000000',
    #     '00012221000000000',
    #     '00012321000000000',
    #     '00012221000000012',
    #     '00011111000000000',
    #     '11100000000000000',
    #     '12100000000000000',
    #     '11100000000000000']) == 52, 'pyramids'
