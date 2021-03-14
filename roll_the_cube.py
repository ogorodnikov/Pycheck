from typing import Set, Tuple


def roll_cube(
    dimensions: Tuple[int, int],
    start: Tuple[int, int],
    colored: Set[Tuple[int, int]],
) -> str:
    """Find a way to color the cube entirely, by rolling it."""


if __name__ == '__main__':
    def checker(data, user_result):
        (nrows, ncols), pos, colored = data
        assert isinstance(user_result, str), 'You must return a string.'
        assert user_result, 'You must return some directions to roll the cube.'
        forbidden_chars = ''.join(sorted(set(user_result) - set('NSWE')))
        assert not forbidden_chars, \
            'You must return NSWE directions, not %r.' % forbidden_chars
        MOVES = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        ROLL = {
            'N': dict(zip('DUNSWE', 'SNDUWE')),
            'S': dict(zip('DUNSWE', 'NSUDWE')),
            'W': dict(zip('DUNSWE', 'EWNSDU')),
            'E': dict(zip('DUNSWE', 'WENSUD')),
        }
        faces = set()
        for nsteps, move in enumerate(user_result, 1):
            (r, c), (dr, dc) = pos, MOVES[move]
            r, c = pos = r + dr, c + dc
            assert 0 <= r < nrows and 0 <= c < ncols, \
                'Step %d: you are outside the grid at %s.' % (nsteps, pos)
            faces = set(map(ROLL[move].get, faces))
            b1 = pos in colored and 'D' not in faces
            b2 = pos not in colored and 'D' in faces
            if b1:
                faces.add('D')
                colored.remove(pos)
            if len(faces) == 6:
                break
            if b2:
                faces.remove('D')
                colored.add(pos)
        else:
            message = 'After %d steps, there are %d face(s) still uncolored.'
            raise AssertionError(message % (nsteps, 6 - len(faces)))
        assert len(user_result) == nsteps, "It's colorful, stop rolling."
        return nsteps

    TESTS = [
        ((4, 2), (2, 1), {(0, 0), (0, 1), (1, 0), (2, 0), (3, 0), (3, 1)}),
        ((3, 3), (2, 1), {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)}),
        ((4, 4), (1, 3), {(0, 0), (1, 2), (2, 1), (3, 0), (3, 2), (3, 3)}),
        ((4, 4), (2, 2), {(0, 0), (0, 3), (1, 2), (2, 1), (3, 0), (3, 3)}),
        ((10, 10), (3, 9), {(0, 4), (2, 9), (3, 8), (4, 0), (4, 9), (7, 7)}),
    ]

    for dimensions, start, colored in TESTS:
        try:
            user_result = roll_cube(dimensions, start, colored.copy())
            print('Your result:', user_result)
            nsteps = checker((dimensions, start, colored.copy()), user_result)
            print('You did it in %d steps.' % nsteps)
        except AssertionError as error:
            print('Test dimensions=%s, start=%s failed:' % (dimensions, start))
            print(error.args[0])
            break
        print()
    else:
        print('Well done! Click on "Check" for more tests.')