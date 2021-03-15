from typing import List, Tuple, Iterable


def rectangles(grid: List[List[int]]) -> Iterable[Tuple[int, int, int, int]]:
    return []


if __name__ == '__main__':
    GRIDS = (
        [[3, 0, 0, 0, 0, 2],
         [2, 0, 0, 4, 0, 0],
         [0, 5, 0, 0, 0, 0],
         [3, 0, 3, 2, 0, 0],
         [0, 0, 2, 0, 0, 6],
         [0, 0, 0, 4, 0, 0]],
        [[6, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 2, 0, 2, 0, 0, 4, 0, 0],
         [0, 0, 0, 0, 0, 0, 5, 0, 0],
         [0, 12, 2, 0, 5, 0, 0, 0, 0],
         [0, 0, 2, 0, 3, 0, 2, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 7],
         [0, 0, 3, 0, 0, 12, 0, 0, 0],
         [0, 2, 0, 0, 0, 4, 0, 0, 4]],
        [[2, 6, 0, 0, 0, 0, 0, 3],
         [0, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 8, 0, 0],
         [4, 0, 0, 2, 0, 0, 0, 0],
         [0, 0, 6, 0, 0, 0, 2, 2],
         [0, 2, 0, 0, 0, 0, 0, 6],
         [2, 0, 0, 0, 0, 0, 0, 0],
         [0, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 8, 0, 0, 0, 0, 0],
         [3, 0, 0, 3, 14, 0, 0, 4],
         [0, 0, 0, 0, 4, 0, 3, 0]],
    )

    def checker(grid, result):
        from itertools import product
        try:
            result = list(result)
        except TypeError:
            raise AssertionError('Your result must be iterable.')
        nb_rects = sum(cell != 0 for row in grid for cell in row)
        if len(result) != nb_rects:
            print(f'There are {nb_rects} rectangles to detect, '
                  f'but you gave {len(result)} rectangle(s).')
        nb_rows, nb_cols = len(grid), len(grid[0])
        colored_grid = [[0 for _ in range(nb_cols)] for _ in range(nb_rows)]
        prev_rects = set()
        for color, rect in enumerate(result, 1):
            assert (isinstance(rect, (tuple, list)) and len(rect) == 4
                    and all(isinstance(coord, int) for coord in rect)), \
                (f'{rect} does not represent a rectangle, '
                 'it should be a tuple/list of four integers.')
            assert tuple(rect) not in prev_rects, \
                f'You gave the same rectangle {rect} twice.'
            prev_rects.add(tuple(rect))
            x1, y1, x2, y2 = rect
            assert x1 <= x2 and y1 <= y2, \
                (f'The rectangle {rect} must be '
                 '(top left coords, bottom right coords).')
            for x, y in ((x1, y1), (x2, y2)):
                assert 0 <= x < nb_rows and 0 <= y < nb_cols, \
                    (f'The rectangle {rect} contains {x, y} '
                     'which is not in the grid.')
            area = (x2 + 1 - x1) * (y2 + 1 - y1)
            grid_area = None
            for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
                assert not colored_grid[x][y], \
                    (f'Rectangle #{color} intersects '
                     f'rectangle #{colored_grid[x][y]} at {x, y}.')
                colored_grid[x][y] = color
                if grid[x][y]:
                    assert grid_area is None, \
                        (f'The rectangle {rect} contains two area values: '
                         f'{grid_area} and {grid[x][y]}.')
                    grid_area = grid[x][y]
                    assert grid[x][y] == area, \
                        (f'The rectangle {rect} have area={area} '
                         f'and contains another area value: {grid[x][y]}.')
            assert grid_area is not None, f'{rect} contains no area value.'
        nb_uncovered = sum(not cell for row in colored_grid for cell in row)
        assert not nb_uncovered, f'{nb_uncovered} cells are still not covered.'

    for test_nb, grid in enumerate(GRIDS, 1):
        result = rectangles([row[:] for row in grid])
        try:
            checker(grid, result)
        except AssertionError as error:
            print(f'You failed the test #{test_nb}:')
            print(error.args[0])
            break
    else:
        print('Well done! Click on "Check" for bigger tests.')
