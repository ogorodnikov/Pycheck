from itertools import product, combinations


def print_chessboard(positions):
    print(' abcdefgh')
    for r in range(7, -1, -1):
        rank = str(r + 1)
        row = rank
        for f in range(8):
            file = chr(97 + f)
            position = file + rank
            if position in positions:
                row += 'X'
            else:
                row += ' '
        print(row)


def get_coverage_of_queens(positions):
    coverage_squares = set()
    for position in positions:
        queen_file_string, queen_rank_string = position
        queen_file = ord(queen_file_string) - 96
        queen_rank = int(queen_rank_string)

        for rank in range(1, 9):
            for file in range(1, 9):
                delta = abs(queen_file - file)
                ranks = (queen_rank - delta, queen_rank, queen_rank + delta)
                if rank in ranks or file == queen_file:
                    coverage_square = (chr(96 + file) + str(rank))
                    coverage_squares.add(coverage_square)

    return coverage_squares


def queens_fit(queens):
    covered = set()
    for queen in queens:
        if queen in covered:
            return False
        covered |= get_coverage_of_queens([queen])
    return True


def place_queens(placed):
    print('Placed:', placed)
    if not queens_fit(placed):
        print('Placed queens do not fit')
        print()
        return set()

    all_squares = {file + rank for file, rank in product('abcdefgh', '12345678')}
    print('All squares:', all_squares)

    uncovered_squares = all_squares - get_coverage_of_queens(placed)
    print('Uncovered squares:')
    print_chessboard(uncovered_squares)

    placements = combinations(uncovered_squares, 8 - len(placed))

    for placement in placements:
        current_uncovered = uncovered_squares.copy()
        placed_queens = placed.copy()

        for new_queen in placement:
            if new_queen not in current_uncovered:
                break

            current_uncovered -= get_coverage_of_queens({new_queen})
            placed_queens |= {new_queen}

            if len(placed_queens) == 8:
                print('Placed 8 queens:', placed_queens)
                print_chessboard(placed_queens)
                print()
                return placed_queens

    print('Unfortunately, placement is not possible')
    print()
    return set()


if __name__ == '__main__':
    from itertools import combinations, product

    COLS = "abcdefgh"
    ROWS = "12345678"

    THREATS = {c + r: set(
        [c + ROWS[k] for k in range(8)] +
        [COLS[k] + r for k in range(8)] +
        [COLS[k] + ROWS[i - j + k] for k in range(8) if 0 <= i - j + k < 8] +
        [COLS[k] + ROWS[- k + i + j] for k in range(8) if 0 <= - k + i + j < 8])
               for i, r in enumerate(ROWS) for j, c in enumerate(COLS)}

    def check_coordinate(coor):
        c, r = coor
        return c in COLS and r in ROWS

    def checker(func, placed, is_possible):
        user_set = func(placed.copy())
        if not all(isinstance(c, str) and len(c) == 2 and check_coordinate(c) for c in user_set):
            print("Wrong Coordinates")
            return False
        threats = []
        for f, s in combinations(user_set.union(placed), 2):
            if s in THREATS[f]:
                threats.append([f, s])
        if not is_possible:
            if user_set:
                print("Hm, how did you place them?")
                return False
            else:
                return True
        if not all(p in user_set for p in placed):
            print("You forgot about placed queens.")
            return False
        if is_possible and threats:
            print("I see some problems in this placement.")
            return False
        return True

    # assert checker(place_queens, {"b2", "c4", "d6", "e8"}, True), "1st Example"
    # assert checker(place_queens, {"b2", "c4", "d6", "e8", "a7", "g5"}, False), "2nd Example"

    assert checker(place_queens, {"a1", "h8"}, False)