from itertools import combinations_with_replacement, permutations, groupby


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
        print(f'    {i}/{combinations_count}: {i / combinations_count * 100:.2f}%')

        groups = tuple(sorted(len(list(group[1])) for group in groupby(sorted(combination))))
        print('    Groups:', groups)

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