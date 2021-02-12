from typing import List
from heapq import heappop, heappush

MATRIX_SIZE = 3
VICTORY = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def get_neighbours(index):
    # for neighbor in range(MATRIX_SIZE ** 2):
    #     if abs(index - neighbor) == MATRIX_SIZE:
    #         yield neighbor
    #     if abs(index - neighbor) == 1 and neighbor // MATRIX_SIZE == index // MATRIX_SIZE:
    #         yield neighbor

    # neighbours = (neighbor for neighbor in range(MATRIX_SIZE ** 2) if
    #               abs(index - neighbor) == MATRIX_SIZE or
    #               abs(index - neighbor) == 1
    #               and neighbor // MATRIX_SIZE == index // MATRIX_SIZE)

    # directions = ''
    # for i in range(MATRIX_SIZE ** 2):
    #     if i // MATRIX_SIZE < index // MATRIX_SIZE:
    #         directions += 'U'
    #     elif i // MATRIX_SIZE > index // MATRIX_SIZE:
    #         directions += 'D'
    #     elif i % MATRIX_SIZE < index % MATRIX_SIZE:
    #         directions += 'L'
    #     elif i % MATRIX_SIZE > index % MATRIX_SIZE:
    #         directions += 'R'
    #     else:
    #         directions += ' '

    directions = ('U' if i // MATRIX_SIZE < index // MATRIX_SIZE else
                  'D' if i // MATRIX_SIZE > index // MATRIX_SIZE else
                  'L' if i % MATRIX_SIZE < index % MATRIX_SIZE else
                  'R' if i % MATRIX_SIZE > index % MATRIX_SIZE else ' '
                  for i in range(MATRIX_SIZE ** 2))

    yield from ((neighbor, direction) for neighbor, direction
                in zip(range(MATRIX_SIZE ** 2), directions)
                if abs(index - neighbor)
                in [MATRIX_SIZE] + [1][:neighbor // MATRIX_SIZE == index // MATRIX_SIZE])


def exchange_tiles(a, b, tiles):
    for i, tile in enumerate(tiles):
        if i == a:
            yield tiles[b]
        elif i == b:
            yield tiles[a]
        else:
            yield tiles[i]


def print_matrix(matrix):
    columns = [iter(matrix)] * MATRIX_SIZE
    [print(*row) for row in zip(*columns)]


def get_distance_to_victory(tiles):
    # distance = 0
    # for i, tile in enumerate(tiles):
    #     for j, victory_tile in enumerate(VICTORY):
    #         if tile == victory_tile:
    #             dy = i // MATRIX_SIZE - j // MATRIX_SIZE
    #             dx = i % MATRIX_SIZE - j % MATRIX_SIZE
    #             distance += ((dx ** 2 + dy ** 2) / 2) ** 0.5

    # distance = 0
    # pairs = ((i, j) for i, tile in enumerate(tiles) for j, victory_tile in enumerate(VICTORY) if tile == victory_tile)
    # for i, j in pairs:
    #     id, ir = divmod(i, MATRIX_SIZE)
    #     jd, jr = divmod(j, MATRIX_SIZE)
    #     dy = id - jd
    #     dx = ir - jr
    #     distance += ((dx ** 2 + dy ** 2) / 2) ** 0.5

    distance = sum((sum((i - j)**2 for i, j in zip(divmod(tile_index, MATRIX_SIZE),
                                                   divmod(victory_tile_index, MATRIX_SIZE))) / 2) ** 0.5
                   for tile_index, tile in enumerate(tiles)
                   for victory_tile_index, victory_tile in enumerate(VICTORY)
                   if tile == victory_tile)

    return distance


def checkio(puzzle: List[List[int]]) -> str:
    print('Puzzle:', puzzle)

    initial_tiles = tuple(tile for row in puzzle for tile in row)

    tick = 0
    q = [(0, initial_tiles, set(), '', tick, 0)]
    while q:
        priority, tiles, history, moves, _, level = heappop(q)

        if tiles in history:
            continue

        if tiles == VICTORY:
            print('Level:', level, 'tick:', tick)
            print('Returning moves:', moves)
            print()
            return moves

        empty_cell = tiles.index(0)
        for neighbour, direction in get_neighbours(empty_cell):
            new_tiles = tuple(exchange_tiles(empty_cell, neighbour, tiles))
            new_priority = get_distance_to_victory(tiles)

            new_entry = (new_priority, new_tiles, history | {tiles}, moves + direction, tick, level + 1)
            heappush(q, new_entry)
            tick += 1

            # print('Level:    ', level, 'tick:', tick)
            # print('Moves:    ', moves)
            # print('Neighbour:', neighbour)
            # print('Direction:', direction)
            # print_matrix(new_tiles)


if __name__ == '__main__':
    GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


    def check_solution(func, puzzle):
        size = len(puzzle)
        route = func([row[:] for row in puzzle])
        goal = GOAL
        x = y = None
        for i, row in enumerate(puzzle):
            if 0 in row:
                x, y = i, row.index(0)
                break
        for ch in route:
            swap_x, swap_y = x + MOVES[ch][0], y + MOVES[ch][1]
            if 0 <= swap_x < size and 0 <= swap_y < size:
                puzzle[x][y], puzzle[swap_x][swap_y] = puzzle[swap_x][swap_y], 0
                x, y = swap_x, swap_y
        if puzzle == goal:
            return True
        else:
            print("Puzzle is not solved")
            return False


    assert check_solution(checkio, [[1, 2, 3],
                                    [4, 6, 8],
                                    [7, 5, 0]]), "1st example"

    assert check_solution(checkio, [[7, 3, 5],
                                    [4, 8, 6],
                                    [1, 2, 0]]), "2nd example"
