import functools
from heapq import heappop, heappush
from itertools import permutations, chain

NEIGHBOURS_4 = (1, 0), (0, 1), (-1, 0), (0, -1)
MAX_ELEVATION_STEP = 1
MIN_MOUNTAIN_HEIGHT = 1
TICK_LIMIT = 10000


def print_map(caption, regional_map):
    map_height = len(regional_map)
    map_width = len(regional_map[0])
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print(caption)
    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y, row in enumerate(regional_map):
        print(f'{y:{row_number_width}d} {row}')


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


def find_tops(elevation_map):
    tops = []
    # islands = []
    checked = []
    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    for y, row in enumerate(elevation_map):
        for x, cell in enumerate(row):
            cell_value = int(cell)
            if cell_value < MIN_MOUNTAIN_HEIGHT:
                continue
            if (x, y) in checked:
                continue
            if is_isolated(x, y, elevation_map):
                continue
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
                    if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                        continue
                    b = bx, by
                    b_value = int(elevation_map[by][bx])
                    if b_value < MIN_MOUNTAIN_HEIGHT or b in checked:
                        continue
                    if b_value > top_value:
                        top_cell = b
                        top_value = b_value
                    q.append(b)
            # yield island_cells
            # yield top_value
            yield top_cell


def distance_cache(function):
    """store path, reversed path and distance"""
    @functools.wraps(function)
    def wrapper_distance_cache(a, b, elevation_map):
        elevation_map = tuple(elevation_map)
        # print('Checking cache for:', a, b)
        if (a, b, elevation_map) not in wrapper_distance_cache.cache:
            path, distance = function(a, b, elevation_map)
            reversed_path = list(reversed(path))
            # print('Calculated:')
            # print('    Path:         ', path)
            # print('    Reversed path:', reversed_path)
            # print('    Distance:     ', distance)
            wrapper_distance_cache.cache[a, b, elevation_map] = path, distance
            wrapper_distance_cache.cache[b, a, elevation_map] = reversed_path, distance
        else:
            print('From cache:')
        return wrapper_distance_cache.cache[a, b, elevation_map]
    wrapper_distance_cache.cache = dict()
    return wrapper_distance_cache


@distance_cache
def get_distance(start, end, elevation_map):
    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    min_path = []
    min_distance = 9999
    tick = 0
    q = [(0, tick, start, [start], 0)]
    while q:
        priority, _, a, path, distance = heappop(q)
        if tick >= TICK_LIMIT:
            # print('Tick limit reached:', TICK_LIMIT)
            break
        if distance >= min_distance:
            continue
        if a == end:
            # print('Shorter path found:', (path, distance))
            min_path = path
            min_distance = distance
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
            heappush(q, (priority, tick, b, path + [b], distance + 1))

    return min_path, min_distance


def climbing_route(elevation_map):
    print_map('Map:', elevation_map)

    top_cells = list(find_tops(elevation_map))
    for top_cell in top_cells:
        print('Top cell:', top_cell)
    print()

    # a, b = (5, 9), (1, 13)
    # print('Get distance:', a, b)
    # path, path_len = get_distance(a, b, elevation_map)
    # print('Distance:', path_len)
    # print('Path:')
    # print_path(path)

    # a, b = (1, 13), (16, 10)
    # print('Get distance:', a, b)
    # path, path_len = get_distance(a, b, elevation_map)
    # print('Distance:', path_len)
    # print('Path:')
    # print_path(path)

    # raise

    map_height = len(elevation_map)
    map_width = len(elevation_map[0])
    start = [(0, 0)]
    end = [(map_width - 1, map_height - 1)]

    route_distances = []
    for permutation in permutations(top_cells):
        pairs = zip(chain(start, permutation), chain(permutation, end))

        print('Route:', *chain(start, permutation, end))
        route_distance = 0
        for pair in pairs:
            print('Pair:', *pair)
            a, b = pair
            path, distance = get_distance(a, b, elevation_map)
            print_path(path)
            print('Distance:', distance)
            print()
            route_distance += distance

        route_distances.append(route_distance)
        print('Route distance:', route_distance)
        print()

    print('Route distances:', route_distances)
    min_route_distance = min(route_distances)
    print('Minimum total distance:', min_route_distance)
    print()
    return min_route_distance


if __name__ == '__main__':


    # assert climbing_route([
    #     '000',
    #     '210',
    #     '000']) == 6, 'basic'

    # assert climbing_route([
    #     '00000',
    #     '05670',
    #     '04980',
    #     '03210',
    #     '00000']) == 26, 'spiral'

    # assert climbing_route([
    #     '000000001',
    #     '222322222',
    #     '100000000']) == 26, 'bridge'
    #
    # assert climbing_route([
    #     '000000120000',
    #     '001002432100',
    #     '012111211000',
    #     '001000000000']) == 16, 'one top'
    #
    # assert climbing_route([
    #     '000000002110',
    #     '011100002310',
    #     '012100002220',
    #     '011100000000']) == 26, 'two top'
    #
    # assert climbing_route([
    #     "01020",
    #     "00304",
    #     "05060",
    #     "00708",
    #     "00000"]) == 8, 'Extra 4'

    assert climbing_route([
        '00000000111111100',
        '00000000122222100',
        '00000000123332100',
        '00000000123432100',
        '00000000123332100',
        '00000000122222100',
        '00000000111111100',
        '00011111000000000',
        '00012221000000000',
        '00012321000000000',
        '00012221000000012',
        '00011111000000000',
        '11100000000000000',
        '12100000000000000',
        '11100000000000000']) == 52, 'pyramids'

