from itertools import tee, zip_longest

FIELD_WIDTH = 4
NEW_TILE_PRIORITIES = list(reversed(range(FIELD_WIDTH ** 2)))
NEW_TILE = 2
EMPTY = 0
GOAL = 2048
VICTORY_BANNER = 'UWIN'
LOSE_BANNER = 'GAMEOVER'


def shift_line(line):
    print('Line:         ', line)

    filtered_line = list(filter(lambda cell: cell != EMPTY, line))
    print('Filtered line:', filtered_line)

    a_iter, b_iter = tee(filtered_line)
    next(b_iter, None)

    shifted_line = []
    for a, b in zip_longest(a_iter, b_iter, fillvalue=EMPTY):
        print('         A, B:', (a, b))

        if a == b:
            shifted_line.append(a + b)
            next(a_iter, None)
            next(b_iter, None)
        else:
            shifted_line.append(a)

    shifted_line += [EMPTY] * (FIELD_WIDTH - len(shifted_line))

    print('Shifted line: ', shifted_line)
    print()
    return shifted_line


def move2048(state, move):
    print('Move:', move)
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
    print()

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
        shifted_field = [list(line) for line in zip(*(row[::-1] for row in shifted_lines))]

    print('Shifted field:')
    [print(line) for line in shifted_field]
    print()

    resulting_field = shifted_field.copy()
    for priority in NEW_TILE_PRIORITIES:
        print('Priority:', priority)

        y, x = divmod(priority, FIELD_WIDTH)
        print('(x, y):', (x, y))

        if resulting_field[y][x] == EMPTY:
            print('Adding 2')
            resulting_field[y][x] = NEW_TILE
            break
    print()

    print('=========================')
    print('Initial move:', move)
    print('Initial state:')
    [print(row) for row in state]
    print()

    print('Resulting field:')
    [print(line) for line in resulting_field]
    print()

    output_field = resulting_field.copy()

    if all(cell != EMPTY for row in shifted_field for cell in row):
        print('No moves left')
        output_field = get_banner(LOSE_BANNER)

    if any(cell == GOAL for row in resulting_field for cell in row):
        print('Goal reached')
        output_field = get_banner(VICTORY_BANNER)

    print('Output field:')
    [print(line) for line in output_field]
    print()
    return output_field


def get_banner(banner_string):
    repetitions_count = FIELD_WIDTH ** 2 // len(banner_string)
    banner_lines = [iter(banner_string * repetitions_count)] * FIELD_WIDTH
    banner = [list(line) for line in zip_longest(*banner_lines)]
    return banner


if __name__ == '__main__':
    # assert move2048([[0, 2, 0, 0],
    #                  [0, 0, 0, 0],
    #                  [0, 0, 0, 0],
    #                  [0, 2, 0, 0]], 'up') == [[0, 4, 0, 0],
    #                                           [0, 0, 0, 0],
    #                                           [0, 0, 0, 0],
    #                                           [0, 0, 0, 2]], "Start. Move Up!"
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
    assert move2048([[4, 4, 0, 0],
                     [0, 4, 1024, 0],
                     [0, 256, 0, 256],
                     [0, 1024, 1024, 8]], 'down') == [['U', 'W', 'I', 'N'],
                                                      ['U', 'W', 'I', 'N'],
                                                      ['U', 'W', 'I', 'N'],
                                                      ['U', 'W', 'I', 'N']], "We are the champions!"

    assert move2048([[2, 4, 8, 16],
                     [32, 64, 128, 256],
                     [512, 1024, 2, 4],
                     [8, 16, 32, 64]], 'left') == [['G', 'A', 'M', 'E'],
                                                   ['O', 'V', 'E', 'R'],
                                                   ['G', 'A', 'M', 'E'],
                                                   ['O', 'V', 'E', 'R']], "Nobody moves!"

    assert move2048([[2, 16, 32, 128],
                     [2, 16, 32, 128],
                     [4, 8, 64, 256],
                     [4, 8, 64, 256]], "down") == [[0, 0, 0, 0],
                                                   [0, 0, 0, 2],
                                                   [4, 32, 64, 256],
                                                   [8, 16, 128, 512]]