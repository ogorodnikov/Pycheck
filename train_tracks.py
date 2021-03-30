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
                if cell in self.empty:
                    row = row[:-1] + 'X'
                if cell == self.start_cell:
                    row = row[:-1] + 'S'
                if cell == self.end_cell:
                    row = row[:-1] + 'E'
            print(row)

    def print_board(self):
        for y in range(len(self.rows)):
            row = ''
            for x in range(len(self.columns)):
                cell = complex(y, x)

                if cell == self.start_cell:
                    letter = 'S'
                elif cell == self.end_cell:
                    letter = 'E'
                elif cell in self.tracks:
                    letter = 'T'
                elif cell in self.empty:
                    letter = 'X'
                else:
                    letter = ':'

                if len(self.exits[cell]) < 4:
                    row += f'{cell:6} {letter} {" ".join(str(e) for e in self.exits[cell]).replace("(-0-1j)", "-j").replace("1j", "j"):10}'
                else:
                    row += f'{"":6} . {" " * 10}'

            print(row)

    def __init__(self, rows, columns, start, end, constraints):

        self.rows = rows
        self.columns = columns
        self.height = len(rows)
        self.width = len(columns)

        self.start_cell, self.end_cell = (complex(y, x) for y, x in (start, end))

        all_cells = {complex(y, x) for x in range(len(columns)) for y in range(len(rows))}
        self.exits = {cell: set(DELTAS) for cell in all_cells}

        shifted_cell_sets = ({cell + delta for cell in all_cells} for delta in DELTAS)
        self.contour_cells = set.union(*(shifted_cells for shifted_cells in shifted_cell_sets)) - all_cells

        self.constraints = {complex(y, x): {DIRECTIONS[d] for d in directions}
                            for (y, x), directions in constraints.items()}
        self.exits.update(self.constraints)

        self.tracks = set()
        self.set_tracks()

        self.cells_per_row = [0] * len(rows)
        self.cells_per_column = [0] * len(columns)

        for cell in self.tracks:
            self.cells_per_row[int(cell.real)] += 1
            self.cells_per_column[int(cell.imag)] += 1

        self.start_cell_exit = next(iter(self.exits[self.start_cell]))

        self.remove_filled_rows_and_columns()
        self.remove_neighbor_exits()
        self.remove_stubs()

    @property
    def empty(self):
        return {cell for cell, exits in self.exits.items() if len(exits) == 0}

    def is_in_board(self, cell):
        return self.height > cell.real >= 0 and self.width > cell.imag >= 0

    def set_tracks(self):
        for a, a_exits in self.constraints.items():
            self.tracks.add(a)
            for a_exit in a_exits:
                b = a + a_exit
                self.tracks.add(b)

    def remove_filled_rows_and_columns(self):
        for row_index, (cells_per_row, row_limit) in enumerate(zip(self.cells_per_row, self.rows)):
            if cells_per_row == row_limit:
                for column_index in range(len(self.columns)):
                    cell = complex(row_index, column_index)
                    if cell in self.tracks:
                        continue
                    self.exits[cell] = set()

    def remove_neighbor_exits(self):

        contour = {cell: set() for cell in self.contour_cells}
        tracks = {cell: self.exits[cell] for cell in self.tracks}
        empty = {cell: self.exits[cell] for cell in self.empty}

        defined = dict()
        defined.update(contour)
        defined.update(tracks)
        defined.update(empty)

        for a, a_exits in defined.items():
            a_missing_exits = set(DELTAS) - a_exits

            for a_missing_exit in a_missing_exits:
                b = a + a_missing_exit

                if b not in self.exits:
                    continue

                b_missing_exit = -a_missing_exit
                self.exits[b] -= {b_missing_exit}

    def remove_stubs(self):

        def get_stubs():
            return {cell: exits for cell, exits in self.exits.items()
                    if len(exits) == 1
                    and cell not in (self.start_cell, self.end_cell)}

        stubs = get_stubs()

        while stubs:
            for stub, stub_exits in stubs.items():
                for stub_exit in stub_exits:
                    b = stub + stub_exit

                    if b not in self.exits:
                        continue

                    b_exit = -stub_exit
                    self.exits[b] -= {b_exit}
                    self.exits[stub] = set()

            stubs = get_stubs()


    def find_path(self):

        tick = 0
        q = [(0, tick, [self.start_cell], self.start_cell_exit,
              self.cells_per_row, self.cells_per_column)]

        while q:

            _, _, path, a_exit, cells_per_row, cells_per_column = heappop(q)
            a = path[-1]
            b = a + a_exit

            if b in path:
                continue

            if b not in self.tracks:
                row_index = int(b.real)
                column_index = int(b.imag)

                if cells_per_row[row_index] == self.rows[row_index]:
                    continue
                if cells_per_column[column_index] == self.columns[column_index]:
                    continue
                cells_per_row[row_index] += 1
                cells_per_column[column_index] += 1

            b_enter = -a_exit
            b_deltas = self.exits[b] - {b_enter}

            if b == self.end_cell:

                final_path = path + [b]

                if not self.check_path(final_path):
                    continue

                moves = self.path_to_moves(final_path)

                self.print_path(final_path)
                print('Tick:', tick)
                print('Final path:', final_path)
                print('Moves string:', moves)

                return moves

            for b_exit in b_deltas:

                if not tick % 100000:
                    print('Tick:', tick)
                    self.print_path(path)
                    print()
                tick += 1

                priority = -tick

                heappush(q, (priority, tick, path + [b], b_exit, list(cells_per_row), list(cells_per_column)))

        raise ValueError

    def check_path(self, final_path):
        if any(cell not in final_path for cell in self.constraints):
            # print('---- Constraint not in final path')
            return False

        if any(sum(int(cell.real) == row_index for cell in final_path) < row_limitation
               for row_index, row_limitation in enumerate(self.rows)):
            # print('---- Row cell count < row limitation')
            return False

        if any(sum(int(cell.imag) == column_index for cell in final_path) < column_limitation
               for column_index, column_limitation in enumerate(self.columns)):
            # print('---- Column cell count < column limitation')
            return False

        return True

    @staticmethod
    def path_to_moves(path):
        moves = [direction for a, b in zip(path, path[1:])
                 for direction, delta in DIRECTIONS.items()
                 if b - a == delta]
        return ''.join(moves)

def train_tracks(rows, columns, start, end, constraints):
    board = TrainBoard(rows, columns, start, end, constraints)

    print('After stubs:')
    board.print_board()
    print()

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
