from itertools import combinations_with_replacement, permutations, groupby


def probability(dice_number, sides, target):

    dice = list(range(1, sides + 1))

    print('Number of dices:', dice_number)
    print('Target:         ', target)
    print('Sides:          ', sides)
    print('Dice:           ', dice)
    print()

    dice_combinations = [combination for combination
                         in combinations_with_replacement(dice, dice_number)
                         if sum(combination) == target]

    combinations_count = len(dice_combinations)
    print('Combinations count:', combinations_count)

    group_dict = {}

    total_fitting_permutations_count = 0
    total_possible_permutations_count = sides ** dice_number

    for i, combination in enumerate(dice_combinations):

        combination_groups = groupby(sorted(combination))
        group_lengths = (len(list(group[1])) for group in combination_groups)
        groups = tuple(sorted(group_lengths))

        if groups in group_dict:
            permutations_count = group_dict[groups]
        else:
            dice_permutations = set(permutations(combination, dice_number))
            permutations_count = len(dice_permutations)
            group_dict[groups] = permutations_count

        total_fitting_permutations_count += permutations_count

        print(f'    {i}/{combinations_count}: {i / combinations_count * 100:.2f}%')
        print('    Combination:       ', combination)
        print('    Groups:            ', groups)
        print('    Permutations count:', permutations_count)
        print('    Total count:       ', total_fitting_permutations_count)
        print()

    target_probability = total_fitting_permutations_count / total_possible_permutations_count

    print('======================')
    print('Total fitting permutations count: ', total_fitting_permutations_count)
    print('Total possible permutations count:', total_possible_permutations_count)
    print('Target probability:               ', target_probability)
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