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

    # field = {key: {complex(x, y)
    #                for y, row in enumerate(board)
    #                for x, cell in enumerate(row)
    #                if cell == key}
    #          for key in {cell for row in board for cell in row}}

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


def get_eaten_counter(stone_groups, field):
    all_cells = {cell for key in field for cell in field[key]}
    eaten_counter = {}

    for color in stone_groups:
        # print('Color:', color)

        eaten_counter[color] = 0
        opposite_color = WHITE if color == BLACK else BLACK

        for stone_group in stone_groups[color]:
            # print('Stone group:', stone_group)

            liberties = {stone + delta for delta in DELTAS for stone in stone_group} - stone_group & all_cells
            # print('    Liberties:', liberties)

            is_group_surrounded = liberties <= field[opposite_color]
            # print('    Is group surrounded:', is_group_surrounded)

            if is_group_surrounded:
                eaten_counter[color] += len(stone_group)

    return eaten_counter


def go_game(board):
    print('Board:')
    [print(row) for row in board]

    field = board_to_field(board)
    # print('Field:', field)

    stone_groups = get_stone_groups(field)
    # print('Stone groups:', stone_groups)

    eaten_counter = get_eaten_counter(stone_groups, field)
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