def is_touching(a, b):

    # intersection = reduce(set.intersection, ({(ax + x, ay + y)
    #                                           for x in range(a_size)
    #                                           for y in range(a_size)}
    #                                          for ax, ay, a_size in (a[1], b[1])))

    a_id, (ax, ay, a_size) = a
    b_id, (bx, by, b_size) = b

    a_squares = {(ax + x, ay + y) for x in range(a_size) for y in range(a_size)}
    b_squares = {(bx + x, by + y) for x in range(b_size) for y in range(b_size)}

    intersection = a_squares & b_squares

    return bool(intersection)


def stacking_cubes(cubes):

    cubes_with_id = [(cube_id, tuple(cube)) for cube_id, cube in enumerate(cubes)]

    connections = {a: {b for b in cubes_with_id
                       if is_touching(a, b)
                       and a is not b}
                   for a in cubes_with_id}

    max_pile_height = max(cube_size for cube_id, (cube_x, cube_y, cube_size) in cubes_with_id)
    q = [[cube] for cube in cubes_with_id]

    while q:
        pile = q.pop()
        a = pile[-1]

        for b in connections[a] - set(pile):

            new_pile = pile + [b]
            new_pile_height = sum(cube_size for cube_id, (cube_x, cube_y, cube_size) in new_pile)
            max_pile_height = max(max_pile_height, new_pile_height)

            q.append(new_pile)

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
