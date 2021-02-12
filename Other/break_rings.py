from itertools import combinations, product


def break_rings(ring_pairs):
    rings = list(set(ring for pair in ring_pairs for ring in pair))
    print('Rings:', rings)
    print('Pairs:', ring_pairs)
    variants = []
    for i in range(1, len(rings)):
        broken_rings_combinations = combinations(rings, i)
        for broken_rings in broken_rings_combinations:
            print('Broken rings:', broken_rings)
            fetched_pairs = [[ring for ring in pair if ring not in broken_rings] for pair in ring_pairs]
            print('Fetched pairs:', fetched_pairs)
            all_unchained = all(len(pair) < 2 for pair in fetched_pairs)
            print('All unchained:', all_unchained)
            rings_left = list(set(ring for pair in fetched_pairs for ring in pair))
            print('Rings left:', rings_left)
            # if all(pair & set(broken_rings) for pair in ring_pairs):
            #     print('End on &')
            #     return i
            if all_unchained:
                # print('Minimum rings:', min_removed_count)
                # return i
                variants.append((i, rings_left))
            print()

    print('Variants:')
    for variant in variants:
        print(variant)

    sorted_variants = sorted(variants, key=lambda v: (v[0], len(v[1])))
    print('Sorted Variants:')
    for variant in sorted_variants:
        print(variant)

    min_removed_count = sorted_variants[0][0]
    print('Minimum rings:', min_removed_count)

    # print(ring_pairs)
    # print(*product(ring_pairs))
    # print()
    # print(*ring_pairs)
    # print(*product(*ring_pairs))

    return min_removed_count


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert break_rings(({1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {4, 6})) == 3, "example"
    assert break_rings(({1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4})) == 3, "All to all"
    assert break_rings(({5, 6}, {4, 5}, {3, 4}, {3, 2}, {2, 1}, {1, 6})) == 3, "Chain"
    assert break_rings(({8, 9}, {1, 9}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 7}, {8, 7})) == 5, "Long chain"
