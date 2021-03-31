from typing import List, Tuple


def is_touching(a, b):
    ax, ay, a_size = a
    bx, by, b_size = b
    return (ax + a_size > bx >= ax and ay + a_size > by >= ay or
            bx + b_size > ax >= bx and by + b_size > ay >= by)


def stacking_cubes(cubes: List[Tuple[int, int, int]]) -> int:
    print('Cubes:', cubes)
    print()

    connections = {a: {b for b in cubes if is_touching(a, b) and a is not b} for a in cubes}
    print('Connections:', connections)
    print()

    max_pile_height = max(cube[2] for cube in cubes)
    q = [[cube] for cube in cubes]

    while q:

        print()
        print('Q:', q)

        pile = q.pop()
        a = pile[-1]

        print('A:', a)

        for b in connections[a] - set(pile):
            print('    B:', b)

            new_pile = pile + [b]

            new_pile_height = sum(cube[2] for cube in new_pile)
            max_pile_height = max(max_pile_height, new_pile_height)

            q.append(new_pile)
            print('    Q:', q)

    print('==== Max pile height:', max_pile_height)
    print()
    return max_pile_height


if __name__ == '__main__':
    assert stacking_cubes([(0, 0, 2), (1, 1, 2), (3, 2, 2)]) == 4, 'basic'
    assert stacking_cubes([(0, 0, 2), (1, 1, 2), (1, 2, 1), (2, 2, 2)]) == 6, 'basic 2'
    assert stacking_cubes([(0, 0, 2), (2, 0, 2), (2, 0, 2), (0, 2, 2), (0, 2, 2), (0, 2, 2), (0, 2, 2)]) == 8, 'towers'
    assert stacking_cubes([(0, 0, 2), (0, 3, 2), (3, 0, 2)]) == 2, 'no stacking'
    assert stacking_cubes([(-1, -1, 2), (0, 0, 2), (-2, -2, 2)]) == 6, 'negative coordinates'
    print("Coding complete? Click 'Check' to earn cool rewards!")
