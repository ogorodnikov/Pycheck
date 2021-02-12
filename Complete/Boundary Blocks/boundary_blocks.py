from itertools import product, combinations
from typing import List, Tuple, Iterable

NEIGHBOURS_4 = (1, 0), (0, 1), (-1, 0), (0, -1)
BLOCK_CHAR = 'X'


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


def print_cells(cells):
    if not cells:
        print('No cells')
        return
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


def get_neighbours(a, deltas):
    ax, ay = a
    return {(ax + dx, ay + dy) for dx, dy in deltas}


def flood_fill(start, grid, block_char):
    map_height = len(grid)
    map_width = len(grid[0])
    flood_fill_cells = set()
    q = [start]
    while q:
        a = q.pop()
        flood_fill_cells.add(a)
        for b in get_neighbours(a, NEIGHBOURS_4):
            if b in flood_fill_cells:
                continue
            bx, by = b
            if map_width <= bx or bx < 0 or map_height <= by or by < 0:
                continue
            b_value = grid[by][bx]
            if b_value == block_char:
                continue
            q.append(b)
    return flood_fill_cells


def boundary_blocks(grid: List[str]) -> Iterable[Tuple[int]]:
    grid_dimensions = map(len, (grid[0], grid))
    grid_ranges = map(range, grid_dimensions)
    all_cells = set(product(*grid_ranges))
    block_cells = {(x, y) for x, y in all_cells if grid[y][x] == BLOCK_CHAR}

    print('+' * 20)
    print('Grid:')
    print_map(grid)
    print('Block cells:')
    print_cells(block_cells)
    print()

    boundary_cells = set()
    for empty_cell in all_cells - block_cells:
        print('Empty cell:', empty_cell)
        flood_fill_cells = flood_fill(start=empty_cell, grid=grid, block_char=BLOCK_CHAR)
        print('Flood fill region:')
        print_cells(flood_fill_cells)
        print()

        for block_cell in block_cells:
            print('    Block:      ', block_cell)
            neighbours = get_neighbours(block_cell, NEIGHBOURS_4) & all_cells
            print('    Neighbours: ', neighbours)

            is_partly_flooded = set() < neighbours & flood_fill_cells < neighbours
            print('    Partly flooded:', is_partly_flooded)

            if is_partly_flooded:
                boundary_cells.add(block_cell)
            print()

    print('Boundary cells:', boundary_cells)
    print_cells(boundary_cells)

    inverted_cells = {(y, x) for x, y in boundary_cells}
    print('Inverted cells:', inverted_cells)
    print()
    return inverted_cells


if __name__ == '__main__':

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

    assert set(boundary_blocks(
        ["..........X", "...........", "...X.X.X...", ".X..X...X..", "...X...X.X.", "X.......X..", "..X..X.X..X",
         "........X..", ".X..X.X..X.", "...X......X", ".X...X..X..", "...........", "X.....X.X..", "...X.......",
         ".X....X...X", ".......X...", "...X......."])) == {(3, 8), (4, 7), (4, 9), (5, 8)}, '#3 4x4'
