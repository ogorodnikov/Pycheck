from collections import deque
from copy import copy
from itertools import product

INF = float('INF')
VICTORY_VECTORS = ()
RESULTS = ('V', 'L', 'D')


def calculate_victory_vectors():
    global VICTORY_VECTORS
    victory_rows = ({(0, 0), (1, 0), (2, 0)},
                    {(0, 1), (1, 1), (2, 1)},
                    {(0, 2), (1, 2), (2, 2)})
    victory_diagonals = ({(0, 0), (1, 1), (2, 2)},
                         {(0, 2), (1, 1), (2, 0)})
    victory_columns = tuple({tuple(reversed(cell)) for cell in vector} for vector in victory_rows)
    VICTORY_VECTORS = victory_rows + victory_columns + victory_diagonals


def print_tuples(xs, os):
    map_height = 3
    map_width = 3
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(map_height):
        print(f'{y:{row_number_width}d} ', end='')
        for x in range(map_width):
            if (x, y) in xs:
                cell_value = 'X'
            elif (x, y) in os:
                cell_value = 'O'
            else:
                cell_value = ' '
            print(cell_value, end='')
        print('\r')


def check_victory(cells):
    for victory_vector in VICTORY_VECTORS:
        if victory_vector <= cells:
            return True
    return False


def x_and_o(grid, your_mark):
    print('Grid:', grid)
    print('Your mark:', your_mark)
    calculate_victory_vectors()

    blanks, xs, os = set(), set(), set()
    for y, x in product(range(3), repeat=2):
        coordinates = x, y
        value = grid[y][x]
        if value == 'X':
            xs.add(coordinates)
        elif value == 'O':
            os.add(coordinates)
        else:
            blanks.add(coordinates)

    moves = []
    tick, added, turn = 0, 0, 0
    q = deque([(turn, xs, os, blanks, moves)])
    results = {move: {result: [INF] for result in RESULTS} for move in blanks}

    while q:
        turn, xs, os, blanks, moves = q.pop()
        # print('')
        print(f'Tick: {tick} Added: {added} Turn: {turn}')
        # print('    Xs:        ', *xs)
        # print('    Os:        ', *os)
        # print('    Blanks:    ', *blanks)
        # print('    Moves:     ', *moves)
        # print_tuples(xs, os)

        tick += 1
        if tick > 100000:
            print('Tick limit')
            break

        if moves:
            first_move = moves[0]
            # print('First move:', first_move)

            min_victory = min(results[first_move]['V'])
            min_loss = min(results[first_move]['L'])

            # if turn >= min_victory:
            #     # print('--- Cutting: >= min victory')
            #     continue
            #
            # if turn >= min_loss:
            #     # print('--- Cutting: >= min loss')
            #     continue

            if not blanks:
                results[first_move]['D'] += [turn]
                print('=== Draw')

            if check_victory(xs):
                # print('=== X wins on turn:', turn)
                if your_mark == 'X':
                    results[first_move]['V'] += [turn]
                if your_mark == 'O':
                    results[first_move]['L'] += [turn]
            if check_victory(os):
                # print('=== O wins on turn:', turn)
                if your_mark == 'O':
                    results[first_move]['V'] += [turn]
                if your_mark == 'X':
                    results[first_move]['L'] += [turn]

        for your_move in blanks:
            new_os, new_xs, new_blanks = map(copy, (os, xs, blanks))
            new_blanks.discard(your_move)

            if your_mark == 'X':
                new_xs.add(your_move)
                for opponents_move in new_blanks:
                    newest_xs, newest_os, newest_blanks = map(copy, (new_xs, new_os, new_blanks))
                    newest_os.add(opponents_move)
                    newest_blanks.discard(opponents_move)
                    q.append((turn + 1, newest_xs, newest_os, newest_blanks, moves + [your_move]))
                    added += 1

            elif your_mark == 'O':
                new_os.add(your_move)
                for opponents_move in new_blanks:
                    newest_xs, newest_os, newest_blanks = map(copy, (new_xs, new_os, new_blanks))
                    newest_xs.add(opponents_move)
                    newest_blanks.discard(opponents_move)
                    q.append((turn + 1, newest_xs, newest_os, newest_blanks, moves + [your_move]))
                    added += 1

    print('Results:')
    for move, result in results.items():
        print(move, result)

    print('Initial grid:', grid)

    best_move, best_result = min(results.items(), key=lambda item: (min(item[1]['V']), -min(item[1]['L'])))
    print('Best move:', best_move)
    print('Best result:', best_result)
    print()
    return tuple(reversed(best_move))


if __name__ == '__main__':
    from random import choice


    def random_bot(grid, mark):
        empties = [(x, y) for x in range(3) for y in range(3) if grid[x][y] == "."]
        return choice(empties) if empties else (None, None)


    def referee(field):
        lines = (["".join(row) for row in field] + ["".join(row) for row in zip(*field)] +
                 [''.join(row) for row in zip(*[(r[i], r[2 - i]) for i, r in enumerate(field)])])
        if "X" * 3 in lines:
            return "X"
        elif "O" * 3 in lines:
            return "O"
        elif not "." in "".join(lines):
            return "D"
        else:
            return "."


    def check_game(user_func, user_mark, bot_mark, bot_algorithm=random_bot):
        grid = [["."] * 3 for _ in range(3)]
        if bot_mark == "X":
            x, y = bot_algorithm(grid, bot_mark)
            grid[x][y] = "X"
        while True:
            user_result = user_func(tuple("".join(row) for row in grid), user_mark)
            if (not isinstance(user_result, (tuple, list)) or len(user_result) != 2 or
                    not all(isinstance(u, int) and 0 <= u < 3 for u in user_result)):
                print("The result must be a list/tuple of two integers from 0 to 2.")
                return False

            if grid[user_result[0]][user_result[1]] != ".":
                print("You tried to mark the filled cell.")
                return False
            grid[user_result[0]][user_result[1]] = user_mark
            game_result = referee(grid)

            if game_result == "D" or game_result == user_mark:
                return True
            bot_move = bot_algorithm(grid, bot_mark)
            grid[bot_move[0]][bot_move[1]] = bot_mark
            game_result = referee(grid)
            if game_result == bot_mark:
                print("Lost :-(")
                return False
            elif game_result == "D":
                return True

    # assert x_and_o(('..X', 'OXO', '..X'), 'O')

    for _ in range(10):
        assert check_game(x_and_o, "X", "O"), "Random X"
        assert check_game(x_and_o, "O", "X"), "Random O"

    # Grid: ('..X', 'OXO', '..X')
    # Your
    # mark: O
