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

    groups = defaultdict(list)
    new_field = {key: set(value) for key, value in field.items()}

    while True:
        group = set()
        if new_field[WHITE]:

            q = [new_field[WHITE].pop()]
            while q:
                a = q.pop()
                group |= {a}
                # print('A:', a)
                # print('New field WHITE :', new_field[WHITE])
                for b in (a + delta for delta in DELTAS):
                    # print('B:', b)
                    if b in new_field[WHITE]:
                        new_field[WHITE] -= {b}
                        group |= {b}
                        q.append(b)
                # print('New field WHITE :', new_field[WHITE])

            groups[WHITE] += [group]


        # elif new_field[BLACK]:
        #     pass
        else:
            return groups



def get_eaten_counter(stone_groups, field):
    pass


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