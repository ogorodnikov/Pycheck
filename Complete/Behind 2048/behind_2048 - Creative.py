from itertools import tee, zip_longest

EMPTY = 0
GOAL = 2048
NEW_TILE = 2
FIELD_WIDTH = 4
VICTORY_BANNER = 'UWIN'
LOSE_BANNER = 'GAMEOVER'
NEW_TILE_PRIORITIES = list(reversed(range(FIELD_WIDTH ** 2)))

NORMALIZE_TO_LEFT = {'left': lambda lines: lines,
                     'up': lambda lines: zip(*lines),
                     'right': lambda lines: map(reversed, lines),
                     'down': lambda lines: map(reversed, zip(*lines))}

# NORMALIZE_FROM_LEFT = NORMALIZE_TO_LEFT.copy() | {'down': lambda lines: zip(*map(reversed, lines))}
NORMALIZE_FROM_LEFT = NORMALIZE_TO_LEFT.copy()
NORMALIZE_FROM_LEFT.update(down=lambda lines: zip(*map(reversed, lines)))

# ANTIDIAGONAL_FLIP = lambda lines: [row[::-1] for row in lines][::-1]
ANTIDIAGONAL_FLIP = lambda lines: reversed(list(map(list, map(reversed, lines))))


def shift_line(line):
    a_iter, b_iter = tee(filter(lambda cell: cell != EMPTY, line))
    next(b_iter, None)

    # shifted_line = []
    # for a, b in zip_longest(a_iter, b_iter, fillvalue=EMPTY):
    #     if a == b:
    #         shifted_line.append(a + b)
    #         next(a_iter, None)
    #         next(b_iter, None)
    #     else:
    #         shifted_line.append(a)

    shifted_line = [a if a != b else
                    a + b + (0 if next(a_iter, None) and next(b_iter, None) else 0)
                    for a, b in zip_longest(a_iter, b_iter, fillvalue=EMPTY)]

    return shifted_line + [EMPTY] * (FIELD_WIDTH - len(shifted_line))


def move2048(state, move):
    normalized_lines = NORMALIZE_TO_LEFT[move](state)
    shifted_lines = map(shift_line, normalized_lines)
    un_normalized_lines = NORMALIZE_FROM_LEFT[move](shifted_lines)

    new_tile_iter = iter([NEW_TILE])

    resulting_field = map(list, un_normalized_lines)
    resulting_field = ANTIDIAGONAL_FLIP(resulting_field)

    resulting_field = [[cell if cell != EMPTY
                        else next(new_tile_iter, 0)
                        for cell in row]
                       for row in resulting_field]

    resulting_field = ANTIDIAGONAL_FLIP(resulting_field)
    resulting_field = list(resulting_field)

    if all(cell != EMPTY for row in resulting_field for cell in row):
        return get_banner(LOSE_BANNER)

    if any(cell == GOAL for row in resulting_field for cell in row):
        return get_banner(VICTORY_BANNER)

    return resulting_field


def get_banner(banner_string):
    repetitions_count = FIELD_WIDTH ** 2 // len(banner_string)
    banner_iter = iter(banner_string * repetitions_count)
    banner_lines = [banner_iter] * FIELD_WIDTH
    banner = list(map(list, zip_longest(*banner_lines)))
    return banner


if __name__ == '__main__':
    assert move2048([[0, 2, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 2, 0, 0]], 'up') == [[0, 4, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 2]], "Start. Move Up!"
    assert move2048([[4, 0, 0, 0],
                     [0, 4, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 8, 8]], 'right') == [[0, 0, 0, 4],
                                                 [0, 0, 0, 4],
                                                 [0, 0, 0, 0],
                                                 [0, 0, 2, 16]], "Simple right"
    assert move2048([[2, 0, 2, 2],
                     [0, 4, 4, 4],
                     [8, 8, 8, 16],
                     [0, 0, 0, 0]], 'right') == [[0, 0, 2, 4],
                                                 [0, 0, 4, 8],
                                                 [0, 8, 16, 16],
                                                 [0, 0, 0, 2]], "Three merging"
    assert move2048([[256, 0, 256, 4],
                     [16, 8, 8, 0],
                     [32, 32, 32, 32],
                     [4, 4, 2, 2]], 'right') == [[0, 0, 512, 4],
                                                 [0, 0, 16, 16],
                                                 [0, 0, 64, 64],
                                                 [0, 2, 8, 4]], "All right"
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
