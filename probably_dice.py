from itertools import combinations_with_replacement, product, permutations, combinations, groupby


def get_permutations_count(all_sides, dice_count, start_side, target):
    count_per_start_side = 0
    q = [(start_side, 1)]
    while q:
        sides_sum, sides_len = q.pop()

        for b in all_sides:
            new_sides_sum = sides_sum + b
            new_sides_len = sides_len + 1

            if new_sides_sum > target:
                continue

            if new_sides_len == dice_count:
                if new_sides_sum == target:
                    count_per_start_side += 1
                continue

            q.append((new_sides_sum, new_sides_len))
    yield count_per_start_side


def get_fitting_permutations(dice_count, side_count, target):
    all_sides = list(range(1, side_count + 1))
    print('All sides:           ', all_sides)

    for start_side in all_sides:
        print('Start side:', start_side)

        for count_per_start_side in get_permutations_count(all_sides, dice_count, start_side, target):
            print('Count per start side:', count_per_start_side)
            yield count_per_start_side


def probability(dice_number, sides, target):
    print('Dice number:', dice_number)
    print('Sides:      ', sides)
    print('Target:     ', target)
    print()

    total_count = 0

    dice = list(range(1, sides + 1))
    print('Dice:', dice)
    print()

    total_permutations_count = sides ** dice_number

    group_dict = {}

    dice_combinations = [combination for combination
                         in combinations_with_replacement(dice, dice_number)
                         if sum(combination) == target]
    combinations_count = len(dice_combinations)
    print('Combinations count:', combinations_count)

    for i, combination in enumerate(dice_combinations):
        print('    Combination:       ', list(combination))
        print(f'    {i} - {i / total_permutations_count:.10f}%')

        groups = tuple(sorted(len(list(group[1])) for group in groupby(sorted(combination))))
        print('Groups:', groups)

        if groups in group_dict:
            permutations_count = group_dict[groups]
        else:
            dice_permutations = set(permutations(combination, len(combination)))
            permutations_count = len(dice_permutations)
            group_dict[groups] = permutations_count

        print('    Permutations count:', permutations_count)

        total_count += permutations_count
        print('    Total count:       ', total_count)
        print()

    print('======================')
    print('Total count:             ', total_count)
    print('Total permutations count:', total_permutations_count)

    target_probability = total_count / total_permutations_count
    print('Target probability:      ', target_probability)

    # fitting_permutations = get_fitting_permutations(dice_number, sides, target)
    #
    # total_count = 0
    # for count_per_start_side in fitting_permutations:
    #
    #     total_count += count_per_start_side
    #     print('Total count:', total_count)
    #
    #     target_probability = total_count / permutations_count
    #     print('Target probability:', target_probability)

    print()
    return target_probability


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=4):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    assert (almost_equal(probability(2, 6, 3), 0.0556)), "Basic example"
    assert (almost_equal(probability(2, 6, 4), 0.0833)), "More points"
    assert (almost_equal(probability(2, 6, 7), 0.1667)), "Maximum for two 6-sided dice"
    assert (almost_equal(probability(2, 3, 5), 0.2222)), "Small dice"
    assert (almost_equal(probability(2, 3, 7), 0.0000)), "Never!"
    assert (almost_equal(probability(3, 6, 7), 0.0694)), "Three dice"
    assert (almost_equal(probability(10, 10, 50), 0.0375)), "Many dice, many sides"


# [1, 1, 5]
# [1, 5, 1]
# [5, 1, 1]
#
# [1, 3, 3]
# [3, 1, 3]
# [3, 3, 1]
#
# [4, 2, 1]
# [4, 1, 2]
# [2, 1, 4]
# [1, 4, 2]
# [1, 2, 4]
# [2, 4, 1]
#
# [3, 2, 2]
# [2, 3, 2]
# [2, 2, 3]