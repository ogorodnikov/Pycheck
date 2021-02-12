from itertools import combinations_with_replacement

MAX_DOMINO_VALUE = 6
TICK_LIMIT = 10 ** 7


def print_square(square, row_sums, column_sums):
    for row, row_sum in zip(square, row_sums):
        row_string = ''.join(str(cell) if cell is not None
                             else '.' for cell in row)
        print(f'{row_string}│{row_sum}')

    square_size = len(square[0])
    print('─' * square_size + '┘')

    columns_sums_str = ''.join(map(str, column_sums))
    print(columns_sums_str)


def det_diagonal_sums(square):
    square_size = len(square[0])

    diagonal_columns = (((i, i),
                         (i, square_size - i - 1))
                        for i in range(square_size))
    diagonals = zip(*diagonal_columns)
    diagonal_sums = [sum(square[x][y] for x, y in diagonal) for diagonal in diagonals]

    return diagonal_sums


def magic_domino(size, number):
    dominoes = (combinations_with_replacement(range(MAX_DOMINO_VALUE + 1), 2))
    domino_set = set(domino for domino in dominoes if sum(domino) <= number)
    domino_count = size ** 2 // 2

    print('Magical Number:', number)
    print('Domino set:    ', domino_set)
    print('Domino count:  ', domino_count)

    # all_squares = []
    # all_row_sums = []
    # all_column_sums = []

    tick = 0
    q = [([], domino_set)]
    while q:
        tiles, unused_tiles = q.pop()

        for new_tile in unused_tiles:
            new_unused_tiles = unused_tiles - {new_tile}
            for new_tile_with_rotation in {new_tile, new_tile[::-1]}:
                new_tiles = tiles + [new_tile_with_rotation]

                tiles_iter = iter(new_tiles)
                square_width = min(size, len(new_tiles))

                square = []
                for row in itertools.zip_longest(*[tiles_iter] * square_width, fillvalue=(None, None)):
                    for sub_row in zip(*row):
                        square.append(sub_row)

                row_sums = []
                for row in square:
                    row_sum = sum(filter(None, row))
                    row_sums.append(row_sum)

                columns = list(zip(*square))
                column_sums = [sum(filter(None, column)) for column in columns]

                # print_square(square, row_sums, column_sums)

                # if square[0] == (0, 0, 2, 3):
                #     if square[1] == (0, 4, 1, 0):
                #         # if square[2] == (4, 0, 0, 1):
                #         print_square(square, row_sums, column_sums)
                #         print('New tiles:   ', new_tiles)
                #         print('Unused tiles:', unused_tiles)
                #         print()

                tick += 1

                if any(row_sum > number for row_sum in row_sums):
                    continue

                if any(column_sum > number for column_sum in column_sums):
                    continue

                # if len(square) == 2:
                #     if len(square[1]) >= 2:
                #         partial_diagonal_sum = square[0][0] + square[1][1]
                #         print('Partial diagonal sum:', partial_diagonal_sum)
                #         print('Tick:', tick)
                #         if partial_diagonal_sum > number:
                #             print('Partial diagonal sum:', partial_diagonal_sum)
                #             print('Number:', number)
                #             print('Tick:', tick)
                #             continue

                if len(new_tiles) == domino_count:
                    # print('Domino count reached')
                    # all_squares.append(square)
                    # all_row_sums.append(row_sums)
                    # all_column_sums.append(column_sums)

                    print('Length matched - tick:', tick)

                    if all(row_sum == number for row_sum in row_sums):
                        print('Rows matched - tick:', tick)

                        if all(column_sum == number for column_sum in column_sums):
                            print('Columns matched - tick:', tick)

                            diagonal_sums = det_diagonal_sums(square)
                            print('Diagonal sums:', diagonal_sums)

                            if all(diagonal_sum == number for diagonal_sum in diagonal_sums):
                                print('Match found!')
                                print('Tick:', tick)
                                print_square(square, row_sums, column_sums)
                                return square
                    continue

                q.append((new_tiles, new_unused_tiles))

                if tick >= TICK_LIMIT:
                    raise TimeoutError('Tick limit:', TICK_LIMIT)

    print('All traversed')
    print('Tick:', tick)
    # for square, row_sums, column_sums in zip(all_squares, all_row_sums, all_column_sums):
    #     print_square(square, row_sums, column_sums)
    #
    #     if square[0] == (0, 0, 2, 3):
    #         if square[1] == (0, 4, 1, 0):
    #             if square[2] == (4, 0, 0, 1):
    #                 raise
    #     print()

    return None


if __name__ == '__main__':
    import itertools


    def check_data(size, number, user_result):

        # check types
        check_container_type = lambda o: any(map(lambda t: isinstance(o, t), (list, tuple)))
        check_cell_type = lambda i: isinstance(i, int)
        if not (check_container_type(user_result) and
                all(map(check_container_type, user_result)) and
                all(map(lambda row: all(map(check_cell_type, row)), user_result))):
            raise Exception("You should return a list/tuple of lists/tuples with integers.")

        # check sizes
        check_size = lambda o: len(o) == size
        if not (check_size(user_result) and all(map(check_size, user_result))):
            raise Exception("Wrong size of answer.")

        # check is it a possible numbers (from 0 to 6 inclusive)
        if not all(map(lambda x: 0 <= x <= 6, itertools.chain.from_iterable(user_result))):
            raise Exception("Wrong matrix integers (can't be domino tiles)")

        # check is it a magic square
        seq_sum_check = lambda seq: sum(seq) == number
        diagonals_indexes = zip(*map(lambda i: ((i, i), (i, size - i - 1)), range(size)))
        values_from_indexes = lambda inds: itertools.starmap(lambda x, y: user_result[y][x], inds)
        if not (all(map(seq_sum_check, user_result)) and  # rows
                all(map(seq_sum_check, zip(*user_result))) and  # columns
                all(map(seq_sum_check, map(values_from_indexes, diagonals_indexes)))):  # diagonals
            raise Exception("It's not a magic square.")

        # check is it domino square
        tiles = set()
        for x, y in itertools.product(range(size), range(0, size, 2)):
            tile = tuple(sorted((user_result[y][x], user_result[y + 1][x])))
            if tile in tiles:
                raise Exception("It's not a domino magic square.")
            tiles.add(tile)


    check_data(4, 5, magic_domino(4, 5))
    check_data(4, 10, magic_domino(4, 10))
