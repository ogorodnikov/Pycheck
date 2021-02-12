from itertools import product, tee, chain
from typing import List

GRID_SIZE = 4


def pairwise(iterable):
    a, b = tee(iterable)
    next(b)
    yield from zip(a, b)


def checkio(lines_list: List[List[int]]) -> int:
    print('Lines list:', lines_list)

    all_lines = {tuple(sorted(line)) for line in lines_list}
    print('All lines:', all_lines)

    all_edges = []
    for square_size in range(1, GRID_SIZE):
        print('Square size:', square_size)

        top_lefts = [1 + y * GRID_SIZE + x for y, x in product(range(GRID_SIZE - square_size), repeat=2)]
        for top_left in top_lefts:
            print('Top left:', top_left)

            square_vertices = (top_left,
                               top_left + square_size,
                               top_left + square_size + square_size * GRID_SIZE,
                               top_left + square_size * GRID_SIZE,
                               top_left)

            pairs = pairwise(square_vertices)
            steps = (1, GRID_SIZE, 1, GRID_SIZE)

            edges_alt2 = set(chain.from_iterable(pairwise(range(start, end + 1, step))
                                             for pair, step in zip(pairs, steps)
                                             for start, end in [sorted(pair)]))
            print('Edges alt 2:', edges_alt2)

            a = top_left
            b = top_left + square_size
            s = 1
            edges_right_alt = list(pairwise(range(a, b + 1, s)))
            print('Edges right alt:', edges_right_alt)

            a = top_left + square_size
            b = top_left + square_size + square_size * GRID_SIZE
            s = GRID_SIZE
            edges_down_alt = list(pairwise(range(a, b + 1, s)))
            print('Edges down alt:', edges_down_alt)

            a = top_left + square_size * GRID_SIZE
            b = top_left + square_size * GRID_SIZE + square_size
            s = 1
            edges_left_alt = list(pairwise(range(a, b + 1, s)))
            print('Edges left alt:', edges_left_alt)

            a = top_left
            b = top_left + square_size * GRID_SIZE
            s = GRID_SIZE
            edges_up_alt = list(pairwise(range(a, b + 1, s)))
            print('Edges up alt:', edges_up_alt)

            edges_alt = list(chain(edges_right_alt, edges_down_alt, edges_left_alt, edges_up_alt))
            print('Edges alt:  ', edges_alt)
            print('Edges alt 2:', edges_alt2)

            print()

            all_edges.append(edges_alt2)

    print('All edges:', all_edges)
    print()

    square_count = sum(edges <= all_lines for edges in all_edges)
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
