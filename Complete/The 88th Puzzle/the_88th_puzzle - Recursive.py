GOAL = (1, 2, 1, 0, 2, 0, 0, 3, 0, 4, 3, 4)
INDICES_FROM = (0, 3, 5, 2)
INDICES_TO = (2, 0, 3, 5)
CIRCLE_COUNT = 4


def rotate_marbles(marbles, circle):
    offset = circle // 2 * 5 + circle % 2
    # the_same_offset = sum(a * b for a, b in zip(divmod(circle, 2), (5, 1)))

    for index, marble in enumerate(marbles):
        for i, index_from in enumerate(INDICES_FROM):
            if index - offset == index_from:
                index_to = INDICES_TO[i] + offset
                yield marbles[index_to]
                break
        else:
            yield marble


def find_rotations(marbles_combinations, checked):

    next_level_marbles_combinations = []

    for marbles, rotations in marbles_combinations:
        if marbles in checked:
            print('- Skip branch')
            continue
        print('+ Check branch')
        if marbles == GOAL:
            return rotations
        checked.append(marbles)

        for circle in range(CIRCLE_COUNT):
            new_marbles = tuple(rotate_marbles(marbles, circle))
            new_rotations = rotations + str(circle + 1)
            next_level_marbles_combinations.append((new_marbles, new_rotations))

    return find_rotations(next_level_marbles_combinations, checked)


def puzzle88(state):
    print('State:', state)

    rotations = find_rotations([(state, '')], [])
    print('Rotations:', rotations)
    print()
    return rotations


if __name__ == '__main__':
    assert puzzle88((1, 2, 1, 0, 2, 0, 0, 3, 0, 4, 3, 4)) == ''
    assert puzzle88((0, 2, 1, 0, 2, 1, 0, 3, 0, 4, 3, 4)) == '1'
    assert puzzle88((0, 2, 1, 0, 2, 1, 4, 3, 0, 4, 3, 0)) in ('14', '41')
    assert puzzle88((0, 2, 1, 0, 2, 1, 4, 3, 4, 0, 3, 0)) in ('144', '414', '441')
    assert puzzle88((0, 2, 1, 3, 2, 1, 4, 0, 0, 4, 0, 3)) in ('1433', '4133'), "Example"
    assert puzzle88((0, 2, 1, 2, 0, 0, 4, 1, 0, 4, 3, 3)) in ('4231', '4321'), "Rotate all"
    assert puzzle88((0, 2, 1, 2, 4, 0, 0, 1, 3, 4, 3, 0)) in ('2314', '2341', '3214', '3241'), "Four paths"
