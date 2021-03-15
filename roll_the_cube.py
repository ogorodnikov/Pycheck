from heapq import heappop, heappush

NEIGHBOURS = 1j, 1, -1j, -1
DIRECTIONS = 'ESWN'
FACES_COUNT = 6


class Cube:

    def __init__(self):
        self.equator = [1, 2, 6, 5]
        self.meridian = [1, 4, 6, 3]
        self.colored = set()

    rotate_right = staticmethod(lambda perimeter: perimeter.append(perimeter.pop(0)))
    rotate_left = staticmethod(lambda perimeter: perimeter.insert(0, perimeter.pop()))

    @staticmethod
    def copy_even_elements(a, b):
        a[0], a[2] = b[0], b[2]

    def turn(self, direction):

        if direction == 'E':
            self.rotate_right(self.equator)
            self.copy_even_elements(self.meridian, self.equator)

        elif direction == 'W':
            self.rotate_left(self.equator)
            self.copy_even_elements(self.meridian, self.equator)

        elif direction == 'S':
            self.rotate_right(self.meridian)
            self.copy_even_elements(self.equator, self.meridian)

        elif direction == 'N':
            self.rotate_left(self.meridian)
            self.copy_even_elements(self.equator, self.meridian)

    @property
    def current_face(self):
        return self.equator[0]

    def paint(self, face):
        self.colored.add(face)

    def copy(self):
        new_cube = Cube()
        new_cube.equator = self.equator.copy()
        new_cube.meridian = self.meridian.copy()
        new_cube.colored = self.colored.copy()
        return new_cube


def roll_cube(dimensions, start, colored):

    height, width = dimensions
    map_colored = {complex(re, im) for re, im in colored}
    all_cells = {complex(re, im) for im in range(width) for re in range(height)}

    tick = 0
    history = set()
    q = [(0, tick, complex(*start), Cube(), map_colored, '')]

    while q:
        priority, _, a, cube, map_colored, path = heappop(q)

        for b, direction in ((a + neighbour, direction) for neighbour, direction
                             in zip(NEIGHBOURS, DIRECTIONS)
                             if a + neighbour in all_cells):

            new_map_colored = map_colored.copy()
            new_cube = cube.copy()

            new_cube.turn(direction)

            if new_cube.current_face not in new_cube.colored and b in map_colored:
                new_map_colored.remove(b)
                new_cube.colored.add(new_cube.current_face)

            if new_cube.current_face in new_cube.colored and b not in map_colored:
                new_cube.colored.remove(new_cube.current_face)
                new_map_colored.add(b)

            uncolored_count = FACES_COUNT - len(new_cube.colored)

            if uncolored_count == 0:
                return path + direction

            current_hash = hash((b, tuple(new_cube.colored), tuple(new_map_colored)))
            if current_hash in history:
                continue
            history.add(current_hash)

            priority = uncolored_count

            tick += 1
            new_entry = (priority, tick, b, new_cube, new_map_colored, path + direction)
            heappush(q, new_entry)


if __name__ == '__main__':

    is_checking = True

    if is_checking:
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
