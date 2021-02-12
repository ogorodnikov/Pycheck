from collections import defaultdict
from itertools import product
from copy import deepcopy

BLANK = '.'
BOARD_SIZE = 3
INF = float('INF')
VICTORY_VECTORS = ()


def calculate_victory_vectors():
    global VICTORY_VECTORS
    victory_rows = ({(0, 0), (1, 0), (2, 0)},
                    {(0, 1), (1, 1), (2, 1)},
                    {(0, 2), (1, 2), (2, 2)})
    victory_diagonals = ({(0, 0), (1, 1), (2, 2)},
                         {(0, 2), (1, 1), (2, 0)})
    victory_columns = tuple({tuple(reversed(cell)) for cell in vector} for vector in victory_rows)
    VICTORY_VECTORS = victory_rows + victory_columns + victory_diagonals


def get_marks(grid):
    marks = defaultdict(set)
    for y, x in product(range(BOARD_SIZE), repeat=2):
        value = grid[y][x]
        marks[value] |= {(x, y)}
    return marks


def print_tuples(marks):
    map_height = map_width = BOARD_SIZE
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print('=' * 20)
    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(map_height):
        print(f'{y:{row_number_width}d} ', end='')
        for x in range(map_width):
            cell_value = (mark for mark, coordinates in marks.items() if (x, y) in coordinates)
            print(*cell_value, end='')
        print('\r')


def check_victory(cells):
    for victory_vector in VICTORY_VECTORS:
        if victory_vector <= cells:
            return True
    return False


def opposite_mark(your_mark):
    return tuple({'X', 'O'} - {your_mark})[0]


def minimax(marks, your_mark, alpha, beta, is_maximising=False):
    if check_victory(marks[your_mark]):
        return 1
    if check_victory(marks[opposite_mark(your_mark)]):
        return -1
    if not marks[BLANK]:
        return 0

    if is_maximising:
        best_score = -INF
        current_mark = your_mark
        operator = max
    else:
        best_score = INF
        current_mark = opposite_mark(your_mark)
        operator = min

    for move in marks[BLANK]:
        new_marks = {mark: {move for move in moves} for mark, moves in marks.items()}
        new_marks[BLANK] -= {move}
        new_marks[current_mark] |= {move}
        score = minimax(new_marks, your_mark, alpha, beta, is_maximising=not is_maximising)
        best_score = operator(score, best_score)

        if is_maximising:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)

        if beta <= alpha:
            break

    return best_score


def x_and_o(grid, your_mark):
    print('Grid:')
    for row in grid:
        print(row)
    print('Your mark:', your_mark)
    calculate_victory_vectors()
    marks = get_marks(grid)

    if len(marks[BLANK]) > BOARD_SIZE ** 2 - 1:
        first_move = list(marks[BLANK])[0]
        return first_move

    best_score = -INF
    best_move = None
    for move in marks[BLANK]:
        print('Move: ', move)
        new_marks = deepcopy(marks)
        new_marks[BLANK] -= {move}
        new_marks[your_mark] |= {move}

        score = minimax(new_marks, your_mark, alpha=-INF, beta=INF)
        print('Score:', score)
        if score > best_score:
            best_score = score
            best_move = move

    print('Best score:', best_score)
    print('Best move: ', best_move)
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


    # assert x_and_o(('..O',
    #                 'X..',
    #                 'OX.'), 'X') == (1, 1)
    #
    # assert x_and_o(('XX.',
    #                 'XO.',
    #                 'OO.'), 'X') == (0, 2)

    # assert check_game(x_and_o, "X", "O"), "Random X"
    # assert check_game(x_and_o, "O", "X"), "Random O"

    for _ in range(10):
        assert check_game(x_and_o, "X", "O"), "Random X"
    for _ in range(10):
        assert check_game(x_and_o, "O", "X"), "Random O"

    # assert x_and_o(('..O',
    #                 '...',
    #                 '.XX'), 'O') == (2, 0)
