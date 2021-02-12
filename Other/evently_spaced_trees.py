from itertools import combinations
from typing import List


def gcd(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif a == b:
        return a
    elif a > b:
        return gcd(a - b, b)
    else:
        return gcd(a, b - a)


def lcm(a, b):
    return abs(a * b) / gcd(a, b)


def evenly_spaced_trees(trees: List[int]) -> int:
    print('Trees:', trees)

    intervals = [b - a for a, b in zip(trees, trees[1:])]
    print('Intervals:', intervals)

    overall_gcd = min(gcd(a, b) for a, b in combinations(intervals, 2))
    print('Overall GCD:', overall_gcd)

    added_trees_range = sorted(range(min(trees), max(trees) + 1, overall_gcd))
    print('Added trees range:', added_trees_range)

    added_trees_count = len(set(added_trees_range) - set(trees))
    print('Added trees count:', added_trees_count)
    print()
    return added_trees_count


if __name__ == '__main__':
    assert evenly_spaced_trees([0, 2, 6]) == 1, 'add 1'
    assert evenly_spaced_trees([1, 3, 6]) == 3, 'add 3'
    assert evenly_spaced_trees([0, 2, 4]) == 0, 'no add'

    assert evenly_spaced_trees([1,52,100]) == 31