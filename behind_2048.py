from itertools import tee

FIELD_WIDTH = 4
NEW_TILE_PRIORITIES = reversed(range(FIELD_WIDTH ** 2))
NEW_TILE = 2
EMPTY = 0


def shift_line(line):
    print('Line:', line)

    filtered_line = list(filter(lambda cell: cell != EMPTY, line))
    print('Filtered line:', filtered_line)

    a_iter, b_iter = tee(filtered_line)
    next(b_iter, None)

    shifted_line = []
    for a, b in zip(a_iter, b_iter):
        print('A:', a)
        print('B:', b)

        if a == b:
            shifted_line.append(a + b)
        else:
            shifted_line.append(a)

    shifted_line += [EMPTY] * (FIELD_WIDTH - len(shifted_line))

    print('Shifted line:', shifted_line)
    print()
    return shifted_line


def move2048(state, move):
    print('State:')
    [print(row) for row in state]
    print()

    lines = []
    if move == 'left':
        lines = state
    elif move == 'up':
        lines = [line for line in zip(*state)]
    elif move == 'right':
        lines = [line[::-1] for line in state]
    elif move == 'down':
        lines = [line[::-1] for line in zip(*state)]

    print('Lines:')
    [print(line) for line in lines]

    shifted_lines = [shift_line(line) for line in lines]
    print('Shifted lines:')
    [print(line) for line in shifted_lines]
    print()

    shifted_field = []
    if move == 'left':
        shifted_field = [list(line) for line in shifted_lines]
    elif move == 'up':
        shifted_field = [list(line) for line in zip(*shifted_lines)]
    elif move == 'right':
        shifted_field = [list(line[::-1]) for line in shifted_lines]
    elif move == 'down':
        shifted_field = [list(line[::-1]) for line in zip(*shifted_lines)]

    print('Shifted field:')
    [print(line) for line in shifted_field]
    print()

    for priority in NEW_TILE_PRIORITIES:
        print('Priority:', priority)

        y, x = divmod(priority, FIELD_WIDTH)
        print('(x, y):', (x, y))

        if shifted_field[y][x] == EMPTY:
            print('Adding 2')
            shifted_field[y][x] = NEW_TILE
            break
    print()

    print('Shifted field with new 2:')
    [print(line) for line in shifted_field]
    print()
    return shifted_field


if __name__ == '__main__':
    assert move2048([[0, 2, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 2, 0, 0]], 'up') == [[0, 4, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 2]], "Start. Move Up!"

    # assert move2048([[4, 0, 0, 0],
    #                  [0, 4, 0, 0],
    #                  [0, 0, 0, 0],
    #                  [0, 0, 8, 8]], 'right') == [[0, 0, 0, 4],
    #                                              [0, 0, 0, 4],
    #                                              [0, 0, 0, 0],
    #                                              [0, 0, 2, 16]], "Simple right"
    # assert move2048([[2, 0, 2, 2],
    #                  [0, 4, 4, 4],
    #                  [8, 8, 8, 16],
    #                  [0, 0, 0, 0]], 'right') == [[0, 0, 2, 4],
    #                                              [0, 0, 4, 8],
    #                                              [0, 8, 16, 16],
    #                                              [0, 0, 0, 2]], "Three merging"
    # assert move2048([[256, 0, 256, 4],
    #                  [16, 8, 8, 0],
    #                  [32, 32, 32, 32],
    #                  [4, 4, 2, 2]], 'right') == [[0, 0, 512, 4],
    #                                              [0, 0, 16, 16],
    #                                              [0, 0, 64, 64],
    #                                              [0, 2, 8, 4]], "All right"
    # assert move2048([[4, 4, 0, 0],
    #                  [0, 4, 1024, 0],
    #                  [0, 256, 0, 256],
    #                  [0, 1024, 1024, 8]], 'down') == [['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N']], "We are the champions!"
    # assert move2048([[2, 4, 8, 16],
    #                  [32, 64, 128, 256],
    #                  [512, 1024, 2, 4],
    #                  [8, 16, 32, 64]], 'left') == [['G', 'A', 'M', 'E'],
    #                                                ['O', 'V', 'E', 'R'],
    #                                                ['G', 'A', 'M', 'E'],
    #                                                ['O', 'V', 'E', 'R']], "Nobody moves!"
