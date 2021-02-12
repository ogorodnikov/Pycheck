from itertools import product
from typing import List

GRID_SIZE = 4


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

            edges_right = []
            left, right = top_left, top_left + 1
            for _ in range(square_size - 1):
                edges_right.append((left, right))
                left, right = left + 1, right + 1
            edges_right.append((left, right))
            print('Edges right:', edges_right)

            edges_down = []
            top, bottom = right, right + GRID_SIZE
            for _ in range(square_size - 1):
                edges_down.append((top, bottom))
                top, bottom = top + + GRID_SIZE, bottom + GRID_SIZE
            edges_down.append((top, bottom))
            print('Edges down:', edges_down)

            edges_left = []
            left, right = bottom - 1, bottom
            for _ in range(square_size - 1):
                edges_left.append((left, right))
                left, right = left - 1, right - 1
            edges_left.append((left, right))
            edges_left.sort()
            print('Edges left:', edges_left)

            edges_up = []
            top, bottom = left - GRID_SIZE, left
            for _ in range(square_size - 1):
                edges_up.append((top, bottom))
                top, bottom = top - GRID_SIZE, bottom - GRID_SIZE
            edges_up.append((top, bottom))
            edges_up.sort()
            print('Edges up:', edges_up)

            edges = edges_right + edges_down + edges_left + edges_up
            print('Edges:', edges)
            print()

            all_edges.append(set(edges))

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
