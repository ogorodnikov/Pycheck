NEIGHBOURS = 1j, 1, -1j, -1


class Grid:
    def __init__(self, rows):

        self.rows = rows
        height = len(rows)
        width = len(rows[0])

        self.all_cells = {complex(y, x): grid[y][x] for x in range(width) for y in range(height)}
        self.number_cells = {cell for cell in self.all_cells
                             if self.all_cells[cell] > 0}
        self.empty_cells = self.all_cells.keys() - self.number_cells

        self.initial_cell = self.number_cells.copy().pop()
        self.number = self.all_cells[self.initial_cell]
        self.rectangle = {self.initial_cell}
        self.used_cells = {self.initial_cell}

        self.complete_rectangles = []

    def __repr__(self):
        rows = '\n'.join(row.__repr__() for row in self.rows)
        stats = f'All cells:    {self.all_cells}    \n' + \
                f'Number cells: {self.number_cells} \n' + \
                f'Empty cells:  {self.empty_cells}  \n'
        return rows + '\n' + stats



def rectangles(grid):
    # print('Grid:')
    # [print(row) for row in grid]
    # print()

    height, width = len(grid), len(grid[0])

    all_cells = {complex(y, x): grid[y][x] for x in range(width) for y in range(height)}
    number_cells = {cell for cell in all_cells if all_cells[cell] > 0}
    empty_cells = all_cells.keys() - number_cells

    # print('All cells:', all_cells)
    # print('Number cells:', number_cells)
    # print('Empty cells:', empty_cells)

    number_cells_iter = iter(number_cells)
    initial_cell = next(number_cells_iter)

    initial_grid = Grid(grid)
    print('Initial grid:', initial_grid)
    quit()

    q = [(initial_cell, all_cells[initial_cell], {initial_cell}, {initial_cell}, [])]

    while q:
        a, number, rectangle, used_cells, complete_rectangles = q.pop()

        for b in (a + delta for delta in NEIGHBOURS):

            if b not in all_cells.keys():
                continue
            if b in used_cells:
                continue
            if b in number_cells:
                continue

            new_rectangle = rectangle | {b}
            new_used_cells = used_cells | {b}

            print('    B:', b)
            print('    New rectangle: ', new_rectangle)
            print('    New used cells:', new_used_cells)

            if len(new_rectangle) == number:
                print('    >>> Rectangle reached len of:', len(new_rectangle))

                rectangle_height = 1 + max(new_rectangle, key=abs).real - min(new_rectangle, key=abs).real
                rectangle_width = 1 + max(new_rectangle, key=abs).imag - min(new_rectangle, key=abs).imag

                print('        Rectangle height:', rectangle_height)
                print('        Rectangle width:', rectangle_width)

                if rectangle_height * rectangle_width == len(new_rectangle):
                    print('    === New rectangle detected:', new_rectangle)

                    if len(new_used_cells) == sum(len(row) for row in grid):
                        raise


                    complete_rectangles.append(new_rectangle)

                    new_number_cells = {cell for cell in all_cells
                                        if all_cells[cell] > 0
                                        and cell not in new_used_cells}
                    new_initial_cell = new_number_cells.copy().pop()
                    number = all_cells[new_initial_cell]
                    new_rectangle = {new_initial_cell}
                    new_used_cells = new_used_cells | {new_initial_cell}
                    b = new_initial_cell

                else:
                    continue

            q.append((b, number, new_rectangle, new_used_cells, complete_rectangles))

    print('Complete rectangles:')
    [print(rectangle) for rectangle in complete_rectangles]

    print_rectangles(grid, complete_rectangles)

    return []


def print_rectangles(grid, rectangles):
    print('Grid:')
    [print(row) for row in grid]
    print()

    height, width = len(grid), len(grid[0])

    rectangle_dict = {i: rectangle for i, rectangle in enumerate(rectangles)}
    print('Rectangle dict:', rectangle_dict)

    for y in range(height):
        row = ''
        for x in range(width):
            cell = complex(y, x)
            print('Cell:', cell)
            for i, rectangle in rectangle_dict.items():
                if cell in rectangle:
                    number = i
                    print('    Number:', number)
            print('Number:', number)
            row += str(number)

        print(row)



if __name__ == '__main__':
    GRIDS = (
        [[3, 0, 0, 0, 0, 2],
         [2, 0, 0, 4, 0, 0],
         [0, 5, 0, 0, 0, 0],
         [3, 0, 3, 2, 0, 0],
         [0, 0, 2, 0, 0, 6],
         [0, 0, 0, 4, 0, 0]],
        # [[6, 0, 0, 0, 0, 0, 0, 2, 0],
        #  [0, 2, 0, 2, 0, 0, 4, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 5, 0, 0],
        #  [0, 12, 2, 0, 5, 0, 0, 0, 0],
        #  [0, 0, 2, 0, 3, 0, 2, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 2, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0, 7],
        #  [0, 0, 3, 0, 0, 12, 0, 0, 0],
        #  [0, 2, 0, 0, 0, 4, 0, 0, 4]],
        # [[2, 6, 0, 0, 0, 0, 0, 3],
        #  [0, 2, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 8, 0, 0],
        #  [4, 0, 0, 2, 0, 0, 0, 0],
        #  [0, 0, 6, 0, 0, 0, 2, 2],
        #  [0, 2, 0, 0, 0, 0, 0, 6],
        #  [2, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 2, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 8, 0, 0, 0, 0, 0],
        #  [3, 0, 0, 3, 14, 0, 0, 4],
        #  [0, 0, 0, 0, 4, 0, 3, 0]],
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
