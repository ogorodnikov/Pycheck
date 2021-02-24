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

    return field


def get_empty_cell_groups(field):
    while field[EMPTY]:
        group = set()
        q = [field[EMPTY].pop()]
        while q:
            cell_a = q.pop()
            group |= {cell_a}
            for cell_b in (cell_a + delta for delta in DELTAS):
                if cell_b in field[EMPTY]:
                    field[EMPTY] -= {cell_b}
                    group |= {cell_b}
                    q.append(cell_b)
        yield group


def get_territory_counter(empty_cell_groups, field):
    all_cells = {cell for key in field for cell in field[key]}
    territory_counter = {BLACK: 0, WHITE: 0}

    for empty_cell_group in empty_cell_groups:
        print('Empty cell group:', empty_cell_group)

        surrounding_cells = {cell + delta for delta in DELTAS for cell in
                             empty_cell_group} - empty_cell_group & all_cells
        print('Surrounding cells:', surrounding_cells)

        if surrounding_cells <= field[WHITE]:
            print('Surrounded by white +', len(empty_cell_group))
            territory_counter[WHITE] += len(empty_cell_group)
        elif surrounding_cells <= field[BLACK]:
            print('Surrounded by black +', len(empty_cell_group))
            territory_counter[BLACK] += len(empty_cell_group)

    return territory_counter


def territory(board):
    print('Board:')
    [print(row) for row in board]

    field = board_to_field(board)
    print('Field:', field)

    empty_cell_groups = get_empty_cell_groups(field)
    print('Empty cell groups:', empty_cell_groups)

    territory_counter = get_territory_counter(empty_cell_groups, field)
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
