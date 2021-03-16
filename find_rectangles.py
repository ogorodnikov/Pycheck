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

        initial_cell = self.number_cells.copy().pop()
        self.number = self.all_cells[initial_cell]
        self.rectangle = {initial_cell}
        self.used_cells = {initial_cell}
        self.current_cell = initial_cell
        self.complete_rectangles = []

    def __repr__(self):
        rows = '\n'.join(row.__repr__() for row in self.rows)
        stats = f'All cells:    {self.all_cells}    \n' + \
                f'Number cells: {self.number_cells} \n' + \
                f'Empty cells:  {self.empty_cells}  \n'
        return rows + '\n' + stats

    def copy(self):
        new_grid = Grid(self.rows)
        new_grid.__dict__.update(self.__dict__)
        return new_grid

    @property
    def is_rectangle(self):
        rectangle_height = 1 + max(self.rectangle, key=abs).real - min(self.rectangle, key=abs).real
        rectangle_width = 1 + max(self.rectangle, key=abs).imag - min(self.rectangle, key=abs).imag

        print('        Rectangle height:', rectangle_height)
        print('        Rectangle width:', rectangle_width)

        return rectangle_height * rectangle_width == len(self.rectangle)

    @property
    def is_all_parsed(self):
        return self.used_cells == set(self.all_cells.keys())

    @property
    def rectangles_coordinates(self):
        raise NotImplementedError
        return self.complete_rectangles


def rectangles(grid):

    initial_grid = Grid(grid)
    print('Initial grid:')
    print(initial_grid)

    q = [initial_grid]

    while q:
        g = q.pop()
        print('Current grid:')
        print(g)

        for b in (g.current_cell + delta for delta in NEIGHBOURS):

            if b not in g.all_cells.keys():
                continue
            if b in g.used_cells:
                continue
            if b in g.number_cells:
                continue

            new_g = g.copy()
            new_g.rectangle = g.rectangle | {b}
            new_g.used_cells = g.used_cells | {b}
            new_g.current_cell = b

            print('    B:', b)
            print('    New rectangle: ', new_g.rectangle)
            print('    New used cells:', new_g.used_cells)

            if len(new_g.rectangle) == new_g.number:
                print('    >>> Rectangle reached len of:', len(new_g.rectangle))
                if new_g.is_rectangle:
                    print('    === New rectangle detected:', new_g.rectangle)
                    quit()

                    if new_g.is_all_parsed:
                        return new_g.rectangles_coordinates

                #     complete_rectangles.append(new_rectangle)
                #
                #     new_number_cells = {cell for cell in all_cells
                #                         if all_cells[cell] > 0
                #                         and cell not in new_used_cells}
                #     new_initial_cell = new_number_cells.copy().pop()
                #     number = all_cells[new_initial_cell]
                #     new_rectangle = {new_initial_cell}
                #     new_used_cells = new_used_cells | {new_initial_cell}
                #     b = new_initial_cell
                #
                # else:
                #     continue

            q.append(new_g)

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
