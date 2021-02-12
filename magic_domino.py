from itertools import combinations_with_replacement, zip_longest
# from timeit import timeit
from random import random, choice

MAX_DOMINO_VALUE = 6
TICK_LIMIT = 10 ** 7


def magic_domino(size, number):
    dominoes = (combinations_with_replacement(range(MAX_DOMINO_VALUE + 1), 2))
    domino_set = list(set(domino for domino in dominoes if sum(domino) <= number))
    domino_count = size ** 2 // 2

    print('Magical Number:', number)
    print('Domino set:    ', domino_set)
    print('Domino count:  ', domino_count)

    tick = 0
    q = [([], domino_set)]
    while q:
        tiles, unused_tiles = q.pop()

        if tick >= TICK_LIMIT:
            raise TimeoutError('Tick limit:', TICK_LIMIT)

        for new_tile_index in range(len(unused_tiles)):
            random_tile_index = choice(range(len(unused_tiles)))
            new_unused_tiles = unused_tiles.copy()
            new_tile = new_unused_tiles.pop(random_tile_index)
            # new_unused_tiles = list(set(new_unused_tiles))
            for new_tile_with_rotation in {new_tile, new_tile[::-1]}:
                new_tiles = tiles + [new_tile_with_rotation]
                tick += 1

                tiles_iter = iter(new_tiles)
                square_width = min(size, len(new_tiles))

                square = []
                for row in zip_longest(*[tiles_iter] * square_width, fillvalue=(None, None)):
                    for sub_row in zip(*row):
                        square.append(sub_row)

                row_sums = [sum(filter(None, row)) for row in square]

                if any(sum(1 for cell in row if cell is not None) == size
                       and row_sum < number
                       or row_sum > number
                       for row, row_sum in zip(square, row_sums)):
                    continue

                columns = list(zip(*square))
                column_sums = [sum(filter(None, column)) for column in columns]

                if any(column_sum > number for column_sum in column_sums):
                    continue

                if any(sum(1 for cell in column if cell is not None) == size
                       and column_sum < number
                       for column, column_sum in zip(columns, column_sums)):
                    continue

                if tick % 1000 == 0:
                    print('Tick:', tick)
                    print_square(square, row_sums, column_sums)


                if len(new_tiles) < domino_count:
                    q.append((new_tiles, new_unused_tiles))
                    continue

                forward_diagonal_sum = sum(square[x][y] for x, y in zip(range(size), range(size)))
                if forward_diagonal_sum != number:
                    continue

                backward_diagonal_sum = sum(square[x][size + ~y] for x, y in zip(range(size), range(size)))
                if backward_diagonal_sum != number:
                    continue

                print('Match found!')
                print('Tick:', tick)
                print_square(square, row_sums, column_sums)
                print()

                return square

    print('All traversed')
    print('Tick:', tick)
    return None


def print_square(square, row_sums, column_sums):
    for row, row_sum in zip(square, row_sums):
        row_string = ''.join('.' if cell is None
                             else str(cell)
                             for cell in row)
        full_string = row_string + '│' + str(row_sum)
        print(full_string)

    square_size = len(square[0])
    print('─' * square_size + '┘')

    column_sum_pairs = (divmod(column_sum, 10) for column_sum in column_sums)
    for column_sum in zip(*column_sum_pairs):
        column_sum_string = ''.join(map(str, column_sum))
        print(column_sum_string)


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


    # check_data(4, 5, magic_domino(4, 5))
    # check_data(4, 8, magic_domino(4, 8))

    # print(timeit(lambda: check_data(4, 14, magic_domino(4, 14)), number=1))
    # print(timeit(lambda: check_data(6, 13, magic_domino(6, 13)), number=1))
    # print(timeit(lambda: check_data(6, 16, magic_domino(6, 16)), number=1))

    check_data(6, 16, magic_domino(6, 16))