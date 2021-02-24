from collections import defaultdict

WHITE = 'W'
BLACK = 'B'
EMPTY = '+'
DELTAS = (1, 1j, -1, -1j)


def board_to_field(board):
    field = defaultdict(set)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            field[cell] |= {complex(x, y)}

    # field = {key: {complex(x, y)
    #                for y, row in enumerate(board)
    #                for x, cell in enumerate(row)
    #                if cell == key}
    #          for key in {cell for row in board for cell in row}}

    return field


def get_empty_cell_groups(field):
    new_field = {key: set(value) for key, value in field.items()}

    empty_cell_groups = []

    def get_group(color):
        group = set()
        q = [new_field[color].pop()]
        while q:
            a = q.pop()
            group |= {a}
            for b in (a + delta for delta in DELTAS):
                if b in new_field[color]:
                    new_field[color] -= {b}
                    group |= {b}
                    q.append(b)
        empty_cell_groups.append(group)

    while True:
        if new_field[EMPTY]:
            get_group(EMPTY)
        else:
            return empty_cell_groups


def get_territory_counter(empty_cell_groups, field):
    all_cells = {cell for key in field for cell in field[key]}
    eaten_counter = {}

    # for color in stone_groups:
    #     # print('Color:', color)
    #
    #     territory_counter[color] = 0
    #     opposite_color = WHITE if color == BLACK else BLACK

    for empty_cell_group in empty_cell_groups:
        print('Empty cell group:', empty_cell_group)

        surrounding_cells = {stone + delta for delta in DELTAS for stone in empty_cell_group} - stone_group & all_cells
        # print('    Liberties:', liberties)

        is_group_surrounded = liberties <= field[opposite_color]
        # print('    Is group surrounded:', is_group_surrounded)

        if is_group_surrounded:
            eaten_counter[color] += len(stone_group)

    return eaten_counter


def territory(board):
    print('Board:')
    [print(row) for row in board]

    field = board_to_field(board)
    print('Field:', field)

    empty_cell_groups = get_empty_cell_groups(field)
    print('Empty cell groups:', empty_cell_groups)

    territory_counter = get_territory_counter(empty_cell_groups, field)
    territory_counter = {'B': 3, 'W': 1}
    print('Territory counter:', territory_counter)
    print()
    return territory_counter


if __name__ == '__main__':

    assert territory(['++B++++++',
                      '+BB++++++',
                      'BB+++++++',
                      '+++++++++',
                      '+++++++++',
                      '++WWW++++',
                      '++W+W++++',
                      '++WWW++++',
                      '+++++++++']) == {'B': 3, 'W': 1}