from collections import deque


def print_map(regional_map):
    "printout map"
    print('=' * 20)
    print(' ' * ((len(regional_map) - 1) // 10 + 2) + ''.join(str(i % 10) for i in range(len(regional_map[0]))))
    for y, row in enumerate(regional_map):
        print(f'{y:{(len(regional_map) - 1) // 10 + 1}d}', end=' ')
        for x, cell in enumerate(row):
            print(regional_map[y][x], end='')
        print('\r')


def finish_map(regional_map):
    print_map(regional_map)

    def get_dutchmans(regional_map):
        for i, row in enumerate(regional_map):
            for j, cell in enumerate(row):
                if cell == 'D':
                    yield (j, i)

    def dutchmanise(regional_map, dutchman):
        new_map = ['...', '...', '...']
        checked = set()
        q = deque([dutchman])
        while q:
            ax, ay = q.pop()
            checked.add((ax, ay))
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                bx, by = max(0, ax + dx), max(0, ay + dy)
                if (bx, by) not in checked \
                        and len(regional_map[0]) > bx >= 0 \
                        and len(regional_map) > by >= 0 \
                        and regional_map[by][bx] == '.':
                    new_map[by][bx] = 'P'
                    q.append((bx, by))
        return regional_map

    for dutchman in get_dutchmans(regional_map):
        regional_map = dutchmanise(regional_map, dutchman)

    print_map(regional_map)

    raise
    return regional_map


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert isinstance(finish_map(("D..", "...", "...")), (list, tuple)), "List or tuple"
    assert list(finish_map(("D..XX.....",
                            "...X......",
                            ".......X..",
                            ".......X..",
                            "...X...X..",
                            "...XXXXX..",
                            "X.........",
                            "..X.......",
                            "..........",
                            "D...X....D"))) == ["DDSXXSDDDD",
                                                "DDSXSSSSSD",
                                                "DDSSSSSXSD",
                                                "DDSSSSSXSD",
                                                "DDSXSSSXSD",
                                                "SSSXXXXXSD",
                                                "XSSSSSSSSD",
                                                "SSXSDDDDDD",
                                                "DSSSSSDDDD",
                                                "DDDSXSDDDD"], "Example"
    assert list(finish_map(("........",
                            "........",
                            "X.X..X.X",
                            "........",
                            "...D....",
                            "........",
                            "X.X..X.X",
                            "........",
                            "........",))) == ["SSSSSSSS",
                                               "SSSSSSSS",
                                               "XSXSSXSX",
                                               "SSSSSSSS",
                                               "DDDDDDDD",
                                               "SSSSSSSS",
                                               'XSXSSXSX',
                                               "SSSSSSSS",
                                               "SSSSSSSS"], "Walls"
