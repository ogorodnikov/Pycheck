from itertools import combinations_with_replacement, permutations, product, repeat, chain

MAX_DOMINO_VALUE = 6
VECTORS = (())


def magic_domino(size, number):
    domino_set = sorted(combinations_with_replacement(range(MAX_DOMINO_VALUE + 1), 2))
    print('Domino set:  ', domino_set)
    print('Number:      ', number)

    domino_count = size ** 2 // 2
    print('Domino count:', domino_count)

    reversion_vectors = list(product((False, True), repeat=domino_count))

    all_index_columns = ((*zip(range(size), repeat(i)),
                          *zip(repeat(i), range(size)),
                          (i, i),
                          (i, size - i - 1))
                         for i in range(size))

    print('All indices:')
    all_indices = list(zip(*all_index_columns))
    for indices in all_indices:
        print('    ', indices)


    for permutation in permutations(domino_set, domino_count):
        print('Permutation:', permutation)

        for reversion_vector in reversion_vectors:
            print('    Reversion vector:', reversion_vector)

            tiles = (tile[::-1] if is_reversed else tile
                     for tile, is_reversed
                     in zip(permutation, reversion_vector))

            square = [sub_row for row in zip(*[tiles] * size) for sub_row in zip(*row)]
            print('        Square:', square)
            for row in square:
                print('            Row:', row)

            if all(sum(square[y][x] for y, x in indices) == number for indices in all_indices):
                print('=== Magic square found:')
                return square


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
