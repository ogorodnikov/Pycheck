from collections import defaultdict

WHITE = 'W'
BLACK = 'B'
EMPTY = '-'
DELTAS = (1, 1j, -1, -1j)


def board_to_field(board):
    field = defaultdict(set)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            field[cell] |= {complex(x, y)}
    return field


def get_stone_groups(field):

    new_field = {key: set(value) for key, value in field.items()}

    groups = defaultdict(list)

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
        groups[color] += [group]

    while True:
        if new_field[WHITE]:
            get_group(WHITE)
        elif new_field[BLACK]:
            get_group(BLACK)
        else:
            return groups


def get_liberties(stone_group):
    liberties = set()
    for stone in stone_group:
        liberties |= {stone + delta for delta in DELTAS}
    liberties -= stone_group
    return liberties


def get_eaten_counter(stone_groups, field):
    print('Field:', field)
    all_cells = {cell for key in field for cell in field[key]}
    print('All cells:', all_cells)
    print('Len all cells :', len(all_cells))

    for color in stone_groups:
        print('Color:', color)
        if color == WHITE:
            opposite_color = BLACK
        else:
            opposite_color = WHITE

        for stone_group in stone_groups[color]:
            print('Stone group:', stone_group)

            liberties = get_liberties(stone_group) & all_cells
            print('    Liberties:', liberties)

            is_group_surrounded = liberties <= field[opposite_color]
            print('    Is group surrounded:', is_group_surrounded)



def go_game(board):
    print('Board:')
    [print(row) for row in board]

    field = board_to_field(board)
    print('Field:', field)

    stone_groups = get_stone_groups(field)
    print('Stone groups:', stone_groups)

    eaten_counter = get_eaten_counter(stone_groups, field)

    eaten_counter = {'B': 3, 'W': 4}

    print('Eaten counter:', eaten_counter)
    print()
    return eaten_counter


if __name__ == '__main__':

    assert go_game(['++++W++++',
                    '+++WBW+++',
                    '++BWBBW++',
                    '+W++WWB++',
                    '+W++B+B++',
                    '+W+BWBWB+',
                    '++++BWB++',
                    '+B++BWB++',
                    '+++++B+++']) == {'B': 3, 'W': 4}