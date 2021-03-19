from copy import deepcopy


class Board:

    def __init__(self, rows):
        self.height = len(rows)
        self.width = len(rows[0])

        self.all_cells = {complex(y, x): rows[y][x]
                          for y in range(self.height)
                          for x in range(self.width)}

        self.number_cells = {cell for cell in self.all_cells
                             if self.all_cells[cell]}

        self.rectangles = [Rectangle(number_cell=cell, board=self)
                           for cell in self.number_cells]

        self.free_cells = self.all_cells.keys() - self.number_cells

    def recalculate_board(self):

        while True:

            possible_count_before = self.possible_rectangles_count

            not_placed_rectangles = filter(lambda r: not r.is_placed,
                                           self.rectangles)
            for rectangle in not_placed_rectangles:
                rectangle.recalculate()

            if self.possible_rectangles_count == possible_count_before:
                print('>>>> Cycling')
                return False

            if all(rectangle.is_placed for rectangle in self.rectangles):
                print('==== Complete')
                return True

    def guess_possible_rectangles(self):

        q = [self]

        while q:
            board = q.pop(0)

            for r_index in range(len(board.rectangles)):

                rectangle = board.rectangles[r_index]
                if rectangle.is_placed:
                    continue

                for guessed in rectangle.possible_rectangles:

                    new_board = deepcopy(board)
                    new_rectangle = new_board.rectangles[r_index]

                    new_rectangle.possible_rectangles = {guessed}
                    new_rectangle.recalculate()

                    if new_board.recalculate_board():
                        return new_board

                    q.append(new_board)

    @property
    def possible_rectangles_count(self):
        return sum(len(r.possible_rectangles) for r in self.rectangles)

    @property
    def rectangles_coordinates(self):
        coordinates = set()
        for rectangle in self.rectangles:
            minimum = min(rectangle.own_cells, key=abs)
            maximum = max(rectangle.own_cells, key=abs)
            rectangle_coordinates = tuple(map(int, (minimum.real, minimum.imag, maximum.real, maximum.imag)))
            coordinates.add(rectangle_coordinates)
        return coordinates


class Rectangle:
    def __init__(self, number_cell, board):
        self.board = board
        self.number_cell = number_cell
        self.number = board.all_cells[number_cell]

        self.guessed_rectangles = set()
        self.own_cells = {self.number_cell}

        self.possible_dimensions = [(height + 1, width + 1)
                                    for width in range(self.board.width)
                                    for height in range(self.board.height)
                                    if (width + 1) * (height + 1) == self.number]

        self.possible_patterns = [{complex(y, x)
                                   for x in range(width)
                                   for y in range(height)}
                                  for height, width
                                  in self.possible_dimensions]

        self.possible_rectangles = {tuple(self.number_cell - shift + delta for delta in pattern)
                                    for pattern in self.possible_patterns
                                    for shift in pattern}

    def recalculate(self):

        for rectangle in self.possible_rectangles.copy():

            available_cells = self.board.free_cells | self.own_cells
            if any(cell not in available_cells for cell in rectangle):
                self.possible_rectangles.remove(rectangle)
                # print('---- Obstacle')
                continue

        common_cells = {cell for rectangle in self.possible_rectangles
                        for cell in rectangle
                        if all(cell in rectangle
                               for rectangle in self.possible_rectangles)}

        self.own_cells = common_cells
        self.board.free_cells -= common_cells

    @property
    def is_placed(self):
        return len(self.own_cells) == self.number


def rectangles(grid):

    board = Board(grid)

    if not board.recalculate_board():
        board = board.guess_possible_rectangles()

    return board.rectangles_coordinates


if __name__ == '__main__':
    GRIDS = (
        [[4, 0, 0, 4],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [4, 0, 0, 4]],
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
        [[0, 0, 0, 2, 0, 3, 4, 0, 4, 0, 0, 0, 3, 0, 0, 2],
         [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 6, 0, 0, 2, 0, 3, 0, 0, 6, 6, 0, 0, 4],
         [0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 16, 0, 4, 0, 0],
         [21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
         [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0]],
        [[0, 0, 2, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0], [4, 9, 0, 3, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0],
         [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
         [0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [6, 0, 0, 0, 0, 0, 0, 6, 0, 10, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0],
         [0, 0, 0, 20, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0], [2, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 2, 3, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 0], [6, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 2, 4, 0, 0],
         [0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3]],
        [[3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0],
         [0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 8, 0, 4],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
         [3, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0],
         [3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0, 4, 0],
         [0, 2, 4, 0, 0, 0, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 0, 0, 0, 12, 0, 0],
         [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
         [2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4]],
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
