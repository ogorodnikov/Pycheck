def get_fitting_permutations(dice_count, side_count, target):

    dice_sides = list(range(1, side_count + 1))
    print('Dice sides:', dice_sides)

    fitting_permutations = []
    q = []


def probability(dice_number, sides, target):
    print('Dice number:', dice_number)
    print('Sides:      ', sides)
    print('Target:     ', target)

    permutations_count = sides ** dice_number
    print('Permutations count:', permutations_count)

    fitting_permutations = get_fitting_permutations(dice_number, sides, target)
    print('Fitting permutations:', fitting_permutations)




    return 0.0556


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=4):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    assert (almost_equal(probability(2, 6, 3), 0.0556)), "Basic example"
    # assert (almost_equal(probability(2, 6, 4), 0.0833)), "More points"
    # assert (almost_equal(probability(2, 6, 7), 0.1667)), "Maximum for two 6-sided dice"
    # assert (almost_equal(probability(2, 3, 5), 0.2222)), "Small dice"
    # assert (almost_equal(probability(2, 3, 7), 0.0000)), "Never!"
    # assert (almost_equal(probability(3, 6, 7), 0.0694)), "Three dice"
    # assert (almost_equal(probability(10, 10, 50), 0.0375)), "Many dice, many sides"
