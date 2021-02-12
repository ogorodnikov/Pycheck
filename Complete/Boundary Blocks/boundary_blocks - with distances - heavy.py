import functools
from heapq import heappop, heappush
from itertools import product, combinations
from typing import List, Tuple, Iterable

NEIGHBOURS_4 = (1, 0), (0, 1), (-1, 0), (0, -1)
TICK_LIMIT = 500000
BLOCK_CHAR = 'X'
INF_VALUE = 9999


def print_map(regional_map):
    if isinstance(regional_map[0], tuple):
        regional_map = [''.join(map(str, row)) for row in regional_map]
    map_height = len(regional_map)
    map_width = len(regional_map[0])
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

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


def distance_cache(function):
    """store path, reversed path and distance"""

    @functools.wraps(function)
    def wrapper_distance_cache(a, b, grid):
        grid = tuple(grid)
        # print('Checking cache for:', a, b)
        if (a, b, grid) not in wrapper_distance_cache.cache:
            path, distance = function(a, b, grid)
            reversed_path = list(reversed(path))
            # print('Calculated:')
            # print('    Path:         ', path)
            # print('    Reversed path:', reversed_path)
            # print('    Distance:     ', distance)
            wrapper_distance_cache.cache[a, b, grid] = path, distance
            wrapper_distance_cache.cache[b, a, grid] = reversed_path, distance
        else:
            print('From cache:')
        return wrapper_distance_cache.cache[a, b, grid]

    wrapper_distance_cache.cache = dict()
    return wrapper_distance_cache


@distance_cache
def get_distance(start, end, grid):
    map_height = len(grid)
    map_width = len(grid[0])
    min_path = []
    min_distance = INF_VALUE
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
            b_value = grid[by][bx]
            if b_value == BLOCK_CHAR:
                continue
            end_x, end_y = end
            manhattan_distance = abs(end_x - bx) + abs(end_y - by)
            priority = manhattan_distance
            tick += 1
            heappush(q, (priority, tick, b, path + [b], distance + 1))

    return min_path, min_distance


def get_neighbours(a, deltas):
    ax, ay = a
    return {(ax + dx, ay + dy) for dx, dy in deltas}


def boundary_blocks(grid: List[str]) -> Iterable[Tuple[int]]:
    print('+' * 20)
    print('Grid:')
    print_map(grid)
    print()
    grid_dimensions = map(len, (grid[0], grid))
    grid_ranges = map(range, grid_dimensions)
    all_cells = set(product(*grid_ranges))
    block_cells = {(x, y) for x, y in all_cells if grid[y][x] == BLOCK_CHAR}
    print('Block cells:')
    print_colony(block_cells)
    print()

    boundary_cells = set()
    for block in block_cells:
        print('Block:', block)
        neighbours = get_neighbours(block, NEIGHBOURS_4) - block_cells & all_cells
        print('Neighbours', neighbours)

        print_colony(neighbours)

        combination_set = set(combinations(neighbours, 2))
        distance_list = []
        print('Combinations:')
        for combination in combination_set:
            path, distance = get_distance(*combination, grid)
            distance_list.append(distance)
            print(*combination, ':', distance)

        is_boundary = INF_VALUE in distance_list
        print('Is bordering:', is_boundary)
        print()

        if is_boundary:
            boundary_cells.add(block)

        # if block in ((8, 7), (9, 8)):
        #     raise

    print('Boundary cells:', *sorted(boundary_cells))
    if boundary_cells:
        print_colony(boundary_cells)
    inversed_boundary_cells_set = {(y, x) for x, y in boundary_cells}
    print('Inversed boundary cells set:', inversed_boundary_cells_set)
    print()
    return inversed_boundary_cells_set


if __name__ == '__main__':
    assert set(boundary_blocks(
        ["..........X", "...........", "...X.X.X...", ".X..X...X..", "...X...X.X.", "X.......X..", "..X..X.X..X",
         "........X..", ".X..X.X..X.", "...X......X", ".X...X..X..", "...........", "X.....X.X..", "...X.......",
         ".X....X...X", ".......X...", "...X......."])) == {[3, 8], [4, 7], [4, 9], [5, 8]}, '#3 4x4'

    assert set(boundary_blocks(['..X',
                                '.X.',
                                'X..'])) == {(0, 2), (1, 1), (2, 0)}, '#1 3x3'

    assert set(boundary_blocks(['...',
                                '.X.',
                                'X..'])) == set(), '#2 3x3'

    assert set(boundary_blocks(['X.X.',
                                '.X..',
                                '..X.',
                                '....'])) == {(0, 0), (0, 2), (1, 1)}, '#3 4x4'
