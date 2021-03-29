from heapq import heappop, heappush

DELTAS = (1j, 1, -1j, -1)
DIRECTIONS = {direction: delta for direction, delta in (zip('ESWN', DELTAS))}


class TrainBoard:

    def print_path(self, path):

        moves = [direction for a, b in zip(path, path[1:])
                 for direction, delta in DIRECTIONS.items()
                 if b - a == delta]

        moves_dict = {cell: move for cell, move in zip(path, moves)}

        for y in range(len(self.rows)):
            row = ''
            for x in range(len(self.columns)):
                cell = complex(y, x)
                if cell in moves_dict:
                    row += moves_dict[cell].replace('E', '>').replace('N', '^').replace('W', '<').replace('S', 'v')
                else:
                    row += '.'
                if cell in self.defined_cells:
                    row = row[:-1] + 'D'
                if cell == self.start_cell:
                    row = row[:-1] + 'S'
                if cell == self.end_cell:
                    row = row[:-1] + 'E'
            print(row)

    def __init__(self, rows, columns, start, end, constraints):

        self.rows = rows
        self.columns = columns
        self.start_cell, self.end_cell = (complex(y, x) for y, x in (start, end))

        all_cells = {complex(y, x) for x in range(len(columns)) for y in range(len(rows))}

        shifted_cell_sets = ({cell + delta for cell in all_cells} for delta in DELTAS)
        self.contour = set.union(*(shifted_cells - all_cells for shifted_cells in shifted_cell_sets))

        self.defined_cells = {complex(y, x): {DIRECTIONS[d] for d in directions}
                              for (y, x), directions in constraints.items()}

        self.cells_per_row = [0] * len(rows)
        self.cells_per_column = [0] * len(columns)

        for cell in self.defined_cells:
            self.cells_per_row[int(cell.real)] += 1
            self.cells_per_column[int(cell.imag)] += 1

        self.start_cell_exit = next(iter(self.defined_cells[self.start_cell]))

    def add_defined_exits(self):

        for a, a_exit in ((a, a_exit) for a, a_exits
                          in self.defined_cells.copy().items()
                          for a_exit in a_exits):

            b = a + a_exit
            b_enter = -a_exit

            print('A:', a)
            print('A exit:', a_exit)
            print('B:', b)

            if b in self.defined_cells:
                continue

            row_index, column_index = int(b.real), int(b.imag)

            self.cells_per_row[row_index] += 1
            self.cells_per_column[column_index] += 1

            self.defined_cells[b] = {b_enter}

            for b_exit in DELTAS:
                if b_exit == b_enter:
                    continue
                if b + b_exit in self.contour:
                    continue
                self.defined_cells[b].add(b_exit)
                print('    B enter:', b_enter)
                print('    B exit:', b_exit)
                print('    self.defined_cells[b]:', self.defined_cells[b])
                # input()

    def add_filled_rows_and_columns(self):
        print('Self rows:', self.rows)
        print('Self cells per row:', self.cells_per_row)

        for row_index, (cells_per_row, row_limit) in enumerate(zip(self.cells_per_row, self.rows)):
            if cells_per_row == row_limit:
                for column_index in range(len(self.columns)):
                    cell = complex(row_index, column_index)
                    if cell not in self.defined_cells:
                        # self.defined_cells[cell] = set()
                        self.contour.add(cell)

        self.print_path([])
        print('Self defined cells:', self.defined_cells)
        # input()

    def find_path(self):

        tick = 0
        q = [(0, tick, [self.start_cell], self.start_cell_exit,
              self.cells_per_row, self.cells_per_column)]

        while q:

            _, _, path, a_exit, cells_per_row, cells_per_column = heappop(q)
            a = path[-1]
            b = a + a_exit

            if b in path or b in self.contour:
                continue

            row_index, column_index = int(b.real), int(b.imag)

            if b not in self.defined_cells:

                if cells_per_row[row_index] == self.rows[row_index]:
                    continue
                if cells_per_column[column_index] == self.columns[column_index]:
                    continue
                cells_per_row[row_index] += 1
                cells_per_column[column_index] += 1

            b_enter = -a_exit

            try:
                b_deltas_defined = self.defined_cells[b]
                if b_enter not in b_deltas_defined:
                    continue

                if b == self.end_cell:
                    final_path = path + [b]

                    if any(cell not in final_path for cell in self.defined_cells):
                        # print('---- Defined cell not in final path')
                        continue

                    if any(sum(int(cell.real) == row_index for cell in final_path) < row_limitation
                           for row_index, row_limitation in enumerate(self.rows)):
                        # print('---- Row cell count < row limitation')
                        continue

                    if any(sum(int(cell.imag) == column_index for cell in final_path) < column_limitation
                           for column_index, column_limitation in enumerate(self.columns)):
                        # print('---- Column cell count < column limitation')
                        continue

                    moves = [direction for a, b in zip(final_path, final_path[1:])
                             for direction, delta in DIRECTIONS.items()
                             if b - a == delta]

                    moves_string = ''.join(moves)

                    self.print_path(final_path)

                    print('Tick:', tick)
                    print('Final path:', final_path)
                    print('Moves string:', moves_string)

                    return moves_string

                b_deltas = b_deltas_defined - {b_enter}

            except KeyError:
                b_deltas = {1j, 1, -1j, -1} - {b_enter}

            for b_exit in b_deltas:

                # unpassed_defined_cells = defined_cells.keys() - set(path)
                #
                # next_defined_cell = min(unpassed_defined_cells,
                #                         key=lambda cell: abs(b + b_exit - cell))
                # priority = abs(b + b_exit - next_defined_cell)

                if not tick % 100000:
                    print('Tick:', tick)
                    self.print_path(path)
                    print()
                tick += 1

                priority = -tick

                heappush(q, (priority, tick, path + [b], b_exit, list(cells_per_row), list(cells_per_column)))

        raise ValueError


def train_tracks(rows, columns, start, end, constraints):
    board = TrainBoard(rows, columns, start, end, constraints)
    board.add_defined_exits()
    board.add_filled_rows_and_columns()
    path_string = board.find_path()
    return path_string


if __name__ == '__main__':
    def checker(test, user_result):
        assert isinstance(user_result, str) and user_result, \
            'You must return a (non-empty) string.'
        MOVES = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        forbidden_chars = ''.join(set(user_result) - MOVES.keys())
        assert not forbidden_chars, ('You can only give N, W, S or E as '
                                     f'directions, not: {forbidden_chars}')
        OPPOSITE = dict(zip('NSWE', 'SNEW'))
        rows, columns, start, end, constraints = test
        path = [start]
        for step, nwse in enumerate(user_result, 1):
            r, c = last = path[-1]
            if last in constraints:
                assert nwse in constraints[last], \
                    f'You can not get out of {last} with {nwse!r}.'
                constraints[last].remove(nwse)
            dr, dc = MOVES[nwse]
            position = r, c = r + dr, c + dc
            assert 0 <= r < len(rows) and 0 <= c < len(columns), \
                f'You are outside the grid at {position} after {step} moves.'
            assert position not in path, \
                f'You can not pass twice at {position}.'
            if position in constraints:
                assert OPPOSITE[nwse] in constraints[position], \
                    f'You can not enter at {position} with {nwse!r}.'
                constraints[position].remove(OPPOSITE[nwse])
            path.append(position)
            if position == end:
                assert len(user_result) == step, \
                    (f'You reached the end after {step} moves, '
                     'why are you continuing?')
                break
        else:
            raise AssertionError(f'After all your {step} moves, '
                                 'you still have not reached the end!')
        constraints = {k: v for k, v in constraints.items() if v}
        assert not constraints, (f'{sum(map(len, constraints.values()))}'
                                 ' constraints not respected.')
        from collections import Counter
        all_res_counts = (('Row', rows, Counter(i for i, _ in path)),
                          ('Column', columns, Counter(j for _, j in path)))
        for row_or_col, lines, res_counts in all_res_counts:
            for i, count in enumerate(lines):
                assert res_counts[i] == count, \
                    (f'{row_or_col} {i}: you passed by {res_counts[i]} cells '
                     f'instead of {count}.')


    TESTS = (
        (
            [4, 6, 5, 3, 1, 3, 3, 4],
            [4, 2, 2, 3, 4, 5, 6, 3],
            (3, 0),
            (7, 6),
            {(3, 0): {'N'}, (4, 7): {'N', 'S'},
             (6, 4): {'E', 'W'}, (7, 6): {'W'}},
        ),
        (
            [8, 7, 7, 5, 5, 3, 2, 3],
            [3, 6, 7, 5, 4, 3, 6, 6],
            (3, 0),
            (7, 3),
            {(1, 2): {'E', 'W'}, (1, 6): {'N', 'W'},
             (3, 0): {'E'}, (7, 3): {'W'}},
        ),
        (
            [6, 7, 5, 6, 4, 3, 6, 4],
            [3, 2, 3, 4, 6, 6, 5, 5, 5, 2],
            (3, 0),
            (7, 4),
            {(1, 3): {'N', 'E'}, (3, 0): {'N'}, (4, 5): {'N', 'E'},
             (5, 6): {'E', 'S'}, (7, 4): {'N'}, (7, 8): {'E', 'W'}},
        ),
        (
            [6, 5, 7, 7, 5, 7, 7, 8, 5, 3],
            [5, 4, 7, 8, 7, 6, 7, 4, 4, 8],
            (1, 0),
            (9, 5),
            {(1, 0): {'N'}, (3, 0): {'E', 'S'}, (4, 5): {'W', 'S'},
             (6, 2): {'W', 'S'}, (6, 4): {'E', 'S'}, (6, 5): {'E', 'W'},
             (8, 3): {'E', 'W'}, (9, 5): {'E'}},
        ),
    )

    from copy import deepcopy

    for n, test in enumerate(TESTS, 1):
        user_result = train_tracks(*deepcopy(test))
        try:
            checker(test, user_result)
        except AssertionError as error:
            print(f'You failed the test #{n}:', *error.args)
            break
    else:
        print('Done! Click on "Check" for bigger tests.')
