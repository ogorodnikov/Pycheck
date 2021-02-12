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


def checkio(grid):
    def get_unused(grid):
        ROW, COL = dict(), dict()
        for j in range(len(grid)):
            COL[j] = set(range(1, 10))
        for i, row in enumerate(grid):
            ROW[i] = set(range(1, 10)) - set(row)
            for j, cell in enumerate(row):
                COL[j] -= {cell}
        return ROW, COL

    def get_minimum_variants(grid):
        ROW, COL = get_unused(grid)
        min_variants = set()
        min_variants_len = 9
        for i in ROW:
            #            print('Checking ROW:', i)
            for j in COL:
                #                print('    Checking CELL:', (i, j), grid[i][j])
                variants = ROW[i] & COL[j]
                #                print('    Variants:', variants)
                if len(variants) < min_variants_len and grid[i][j] == 0:
                    min_variants = variants
                    min_variants_len = len(variants)
                    min_variants_cell = (i, j)
        return min_variants, min_variants_cell

    # main loop
    q = deque([(grid, 0)])
    while q:
        current_grid, level = q.popleft()
        min_variants, min_variants_cell = get_minimum_variants(current_grid)
        print('### Level:', level)
        print('    Minimum variants:', min_variants, min_variants_cell)

        for variant in min_variants:
            new_grid = [[e for e in row] for row in current_grid]
            i, j = min_variants_cell
            new_grid[i][j] = variant
            print('Adding:', variant, 'to level:', level + 1)
            print_map(new_grid)
            print()
            q.append((list(new_grid), level + 1))

        if level == 1:
            raise

    return [[0 for j in range(9)] for i in range(9)]


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([[0, 7, 1, 6, 8, 4, 0, 0, 0],
                    [0, 4, 9, 7, 0, 0, 0, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 0, 0, 0, 0, 5, 0, 4],
                    [0, 0, 0, 3, 0, 7, 0, 0, 0],
                    [2, 0, 3, 0, 0, 0, 0, 9, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 9],
                    [0, 0, 0, 0, 0, 3, 7, 2, 0],
                    [0, 0, 0, 4, 9, 8, 6, 1, 0]]) == [[3, 7, 1, 6, 8, 4, 9, 5, 2],
                                                      [8, 4, 9, 7, 2, 5, 3, 6, 1],
                                                      [5, 6, 2, 9, 3, 1, 4, 7, 8],
                                                      [6, 8, 7, 2, 1, 9, 5, 3, 4],
                                                      [9, 1, 4, 3, 5, 7, 2, 8, 6],
                                                      [2, 5, 3, 8, 4, 6, 1, 9, 7],
                                                      [1, 3, 6, 5, 7, 2, 8, 4, 9],
                                                      [4, 9, 8, 1, 6, 3, 7, 2, 5],
                                                      [7, 2, 5, 4, 9, 8, 6, 1, 3]], "first"
    assert checkio([[5, 0, 0, 7, 1, 9, 0, 0, 4],
                    [0, 0, 1, 0, 3, 0, 5, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 5, 9, 7, 2, 6, 4, 0],
                    [0, 0, 0, 6, 0, 1, 0, 0, 0],
                    [0, 2, 6, 3, 8, 5, 9, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 0, 5, 0, 2, 0, 0],
                    [8, 0, 0, 4, 9, 7, 0, 0, 6]]) == [[5, 6, 8, 7, 1, 9, 3, 2, 4],
                                                      [9, 7, 1, 2, 3, 4, 5, 6, 8],
                                                      [2, 3, 4, 5, 6, 8, 7, 9, 1],
                                                      [1, 8, 5, 9, 7, 2, 6, 4, 3],
                                                      [3, 9, 7, 6, 4, 1, 8, 5, 2],
                                                      [4, 2, 6, 3, 8, 5, 9, 1, 7],
                                                      [6, 1, 9, 8, 2, 3, 4, 7, 5],
                                                      [7, 4, 3, 1, 5, 6, 2, 8, 9],
                                                      [8, 5, 2, 4, 9, 7, 1, 3, 6]], "second"
    print('Local tests done')
