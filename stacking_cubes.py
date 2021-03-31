def is_touching(a, b):

    # intersection = reduce(set.intersection, ({(ax + x, ay + y)
    #                                           for x in range(a_size)
    #                                           for y in range(a_size)}
    #                                          for ax, ay, a_size in (a[1], b[1])))

    ax, ay, a_size = a[1]
    bx, by, b_size = b[1]

    a_squares = {(ax + x, ay + y) for x in range(a_size) for y in range(a_size)}
    b_squares = {(bx + x, by + y) for x in range(b_size) for y in range(b_size)}

    intersection = a_squares & b_squares

    return bool(intersection)


def stacking_cubes(cubes):
    print('Cubes:', cubes)
    # print()

    cubes_with_id = [(cube_id, tuple(cube)) for cube_id, cube in enumerate(cubes)]
    # print('Cubes with id:', cubes_with_id)
    # print()

    connections = {a: {b for b in cubes_with_id
                       if a is not b and is_touching(a, b)}
                   for a in cubes_with_id}

    # print('Connections:', connections)
    # print()

    max_pile_height = max(cube[1][2] for cube in cubes_with_id)
    q = [[cube] for cube in cubes_with_id]

    # all_piles = []

    while q:
        pile = q.pop()
        a = pile[-1]

        # print('A:', a)

        for b in connections[a] - set(pile):
            # print('    B:', b)

            new_pile = pile + [b]

            new_pile_height = sum(cube[1][2] for cube in new_pile)

            if new_pile_height > max_pile_height:
                # print('    ++++ New max pile height:', new_pile_height)
                # print('         New pile:           ', new_pile)
                max_pile_height = new_pile_height

            q.append(new_pile)

            # all_piles.append(new_pile)

    print('==== Max pile height:', max_pile_height)
    print()

    # print('Connections:')
    # [print(key, value) for key, value in connections.items()]
    # print()

    # print('All piles:')
    # [print(pile, sum(cube[1][2] for cube in pile)) for pile in all_piles]
    # print()

    return max_pile_height


if __name__ == '__main__':
    assert stacking_cubes([(0, 0, 2), (1, 1, 2), (3, 2, 2)]) == 4, 'basic'
    assert stacking_cubes([(0, 0, 2), (1, 1, 2), (1, 2, 1), (2, 2, 2)]) == 6, 'basic 2'
    assert stacking_cubes([(0, 0, 2), (2, 0, 2), (2, 0, 2), (0, 2, 2), (0, 2, 2), (0, 2, 2), (0, 2, 2)]) == 8, 'towers'
    assert stacking_cubes([(0, 0, 2), (0, 3, 2), (3, 0, 2)]) == 2, 'no stacking'
    assert stacking_cubes([(-1, -1, 2), (0, 0, 2), (-2, -2, 2)]) == 6, 'negative coordinates'
    assert stacking_cubes(
        [[0, 0, 2], [1, 1, 2], [3, -1, 3], [-3, -2, 3], [0, 2, 2], [3, 1, 4], [-3, 0, 3], [-1, -4, 3], [-1, 2, 2],
         [1, -3, 3], [0, 0, 1]]) == 28
