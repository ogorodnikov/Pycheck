from typing import Tuple, Dict, Set, List

Counts, Coords = List[int], Tuple[int, int]
DIRECTIONS = {direction: delta for direction, delta in (zip('ESWN', (1j, 1, -1j, -1)))}


def train_tracks(rows: Counts, columns: Counts,
                 start: Coords, end: Coords,
                 constraints: Dict[Coords, Set[str]]) -> str:
    start_cell, end_cell = (complex(y, x) for y, x in (start, end))

    all_cells = {complex(y, x): {DIRECTIONS[d] for d in constraints[(y, x)]}
                 if (y, x) in constraints else set()
                 for x in range(len(columns))
                 for y in range(len(rows))}

    q = [(start_cell, all_cells, [])]

    while q:
        a, old_cells, path = q.pop()
        cells = {cell: tile.copy() for cell, tile in old_cells.items()}

        print('A:', a)
        print('Cells a :', cells[a])

        for a_direction, a_exit in DIRECTIONS.items():
            print('A direction:', a_direction)
            print('A exit:', a_exit)
            print('A exit not in cells a :', a_exit not in cells[a])

            if a_exit not in cells[a]:
                continue
            b = a + a_exit
            print('    B:', b)
            print('    B not in cells:', b not in cells)
            print('    path and a_exit == -path[-1]:', path and a_exit == -path[-1])
            if b not in cells:
                continue
            if path and a_exit == -path[-1]:
                continue

            for b_direction, b_exit in DIRECTIONS.items():
                b_enter = -a_exit

                print('        B direction:', b_direction)
                print('        B enter:    ', b_enter)
                print('        B exit:     ', b_exit)
                print()

                if b_enter == a_exit or b_enter == b_exit:
                    continue
                if cells[b] and b_enter not in cells[b]:
                    continue

                cells[b] = {b_enter, b_exit}
                q.append((b, cells, path + [a_exit]))
                print('Q:', q)
                quit()







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
        # (
        #     [8, 7, 7, 5, 5, 3, 2, 3],
        #     [3, 6, 7, 5, 4, 3, 6, 6],
        #     (3, 0),
        #     (7, 3),
        #     {(1, 2): {'E', 'W'}, (1, 6): {'N', 'W'},
        #      (3, 0): {'E'}, (7, 3): {'W'}},
        # ),
        # (
        #     [6, 7, 5, 6, 4, 3, 6, 4],
        #     [3, 2, 3, 4, 6, 6, 5, 5, 5, 2],
        #     (3, 0),
        #     (7, 4),
        #     {(1, 3): {'N', 'E'}, (3, 0): {'N'}, (4, 5): {'N', 'E'},
        #      (5, 6): {'E', 'S'}, (7, 4): {'N'}, (7, 8): {'E', 'W'}},
        # ),
        # (
        #     [6, 5, 7, 7, 5, 7, 7, 8, 5, 3],
        #     [5, 4, 7, 8, 7, 6, 7, 4, 4, 8],
        #     (1, 0),
        #     (9, 5),
        #     {(1, 0): {'N'}, (3, 0): {'E', 'S'}, (4, 5): {'W', 'S'},
        #      (6, 2): {'W', 'S'}, (6, 4): {'E', 'S'}, (6, 5): {'E', 'W'},
        #      (8, 3): {'E', 'W'}, (9, 5): {'E'}},
        # ),
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
