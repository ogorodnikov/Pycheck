from itertools import product, tee


def print_matrix(caption, matrix):
    print(caption)
    for row in matrix:
        print(*row)

def checkio(pattern, image):

    mask = [[3 if pattern_cell == 1 else 2 for pattern_cell in row] for row in pattern]
    print_matrix('Image:', image)
    print_matrix('Pattern:', pattern)
    print_matrix('Mask:', mask)

    for y, row in enumerate(image):
        for x, cell in enumerate(row):
            try:
                # search_deltas, replacement_deltas = tee(product(range(len(pattern)), range(len(pattern[0]))))
                # print('Search deltas:')
                # for dx, dy in search_deltas:
                #     print('dx, dy:', (dx, dy))
                # print()
                # print('Replacement deltas:')
                # for dx, dy in replacement_deltas:
                #     print('dx, dy:', (dx, dy))
                # print()

                search_deltas, replacement_deltas = tee(product(range(len(pattern)), range(len(pattern[0]))))
                # search for pattern
                if all(image[y + dy][x + dx] == pattern[dy][dx] for dy, dx in search_deltas):
                    print('Pattern matched at:', (x, y))
                    # replace with mask
                    for dy, dx in replacement_deltas:
                        image[y + dy][x + dx] = mask[dy][dx]
            except IndexError:
                pass

    print_matrix('Image after replacement:', image)
    print()
    return image


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([[0, 1, 0], [1, 1, 1]],
                   [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
                    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) == [[0, 2, 3, 2, 0, 0, 0, 2, 3, 2],
                                                         [0, 3, 3, 3, 0, 0, 0, 3, 3, 3],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 2, 3, 2, 0, 0, 0],
                                                         [2, 3, 2, 0, 3, 3, 3, 0, 1, 0],
                                                         [3, 3, 3, 0, 0, 0, 0, 0, 1, 1],
                                                         [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                                         [0, 0, 1, 0, 0, 0, 2, 3, 2, 0],
                                                         [0, 1, 1, 0, 0, 0, 3, 3, 3, 0],
                                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
assert checkio([[1, 1], [1, 1]],
               [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]) == [[3, 3, 1],
                                [3, 3, 1],
                                [1, 1, 1]]
assert checkio([[1, 0], [1, 1]],
               [[0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0],
                [1, 0, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [0, 1, 1, 0, 0]]) == [[0, 3, 2, 1, 0],
                                      [0, 3, 3, 0, 0],
                                      [3, 2, 1, 3, 2],
                                      [3, 3, 0, 3, 3],
                                      [0, 1, 1, 0, 0]]
