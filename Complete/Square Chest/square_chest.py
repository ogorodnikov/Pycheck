from itertools import product, tee, chain
from typing import List

GRID_SIZE = 4


def pairwise(iterable):
    a, b = tee(iterable)
    next(b)
    yield from zip(a, b)


def get_squares_edges(square_size):

    top_left_vertices = [row * GRID_SIZE + column + 1
                         for row, column
                         in product(range(GRID_SIZE - square_size), repeat=2)]

    for nw in top_left_vertices:

        ne = nw + square_size
        se = nw + square_size + square_size * GRID_SIZE
        sw = nw + square_size * GRID_SIZE

        square_vertices = (nw, ne, se, sw, nw)

        pairs = pairwise(square_vertices)
        steps = (1, GRID_SIZE, 1, GRID_SIZE)

        edges = chain.from_iterable(pairwise(range(start, end + 1, step))
                                    for pair, step in zip(pairs, steps)
                                    for start, end in [sorted(pair)])

        yield edges


def checkio(lines_list: List[List[int]]) -> int:
    all_lines = {tuple(sorted(line)) for line in lines_list}

    all_edges = chain.from_iterable(get_squares_edges(square_size) for square_size in range(1, GRID_SIZE))
    all_edges_list = list(map(set, all_edges))

    square_count = sum(edges <= all_lines for edges in all_edges_list)

    print('All lines:   ', all_lines)
    print('All edges:   ', all_edges_list)
    print('Square count:', square_count)
    print()

    return square_count


if __name__ == '__main__':
    assert (checkio([[1, 2], [3, 4], [1, 5], [2, 6], [4, 8], [5, 6], [6, 7],
                     [7, 8], [6, 10], [7, 11], [8, 12], [10, 11],
                     [10, 14], [12, 16], [14, 15], [15, 16]]) == 3), "First, from description"
    assert (checkio([[1, 2], [2, 3], [3, 4], [1, 5], [4, 8],
                     [6, 7], [5, 9], [6, 10], [7, 11], [8, 12],
                     [9, 13], [10, 11], [12, 16], [13, 14], [14, 15], [15, 16]]) == 2), "Second, from description"
    assert (checkio([[1, 2], [1, 5], [2, 6], [5, 6]]) == 1), "Third, one small square"
    assert (checkio([[1, 2], [1, 5], [2, 6], [5, 9], [6, 10], [9, 10]]) == 0), "Fourth, it's not square"
    assert (checkio([[16, 15], [16, 12], [15, 11], [11, 10],
                     [10, 14], [14, 13], [13, 9]]) == 0), "Fifth, snake"