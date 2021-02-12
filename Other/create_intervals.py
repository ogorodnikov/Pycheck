from itertools import tee


def pairwise(input_values):
    a, b = tee(input_values)
    next(b, None)
    yield from zip(a, b)


def create_intervals(data):
    print('Data:', data)

    if not data:
        print('Zero length')
        return []
    if len(data) == 1:
        zero_element = list(data)[0]
        intervals = [(zero_element, zero_element)]
        print('Intervals:', intervals)
        return intervals

    pairs = list(pairwise(sorted(data)))

    intervals = []
    start = end = pairs[0][0]
    for a, b in pairs:
        print('Pair:', (a, b))
        if b - a == 1:
            print('    increments')
            end = b
        else:
            print('    interrupts')
            intervals.append((start, end))
            start = b
            end = b
    intervals.append((start, end))

    print('Intervals:', intervals)
    print()

    return intervals


if __name__ == '__main__':
    assert create_intervals({1, 2, 3, 4, 5, 7, 8, 12}) == [(1, 5), (7, 8), (12, 12)], "First"
    assert create_intervals({1, 2, 3, 6, 7, 8, 4, 5}) == [(1, 8)], "Second"
    assert create_intervals([1, 3, 7]) == [(1, 1), (3, 3), (7, 7)], "Extra 1"
    assert create_intervals([1]) == [(1, 1)], "Single value"
    assert create_intervals([]) == [], "Empty list"
