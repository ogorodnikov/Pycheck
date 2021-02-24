def get_fitting_permutations(dice_count, side_count, target):

    all_sides = list(range(1, side_count + 1))
    print('All sides:           ', all_sides)

    fitting_permutations = []

    for start_side in all_sides[::-1]:
        print('Start side:', start_side)
        q = [[start_side]]
        while q:
            sides = q.pop()

            for b in all_sides:
                new_sides = sides + [b]
                new_sides_sum = sum(new_sides)
                print('New sides:    ', new_sides)
                print('New sides sum:', new_sides_sum)

                if new_sides_sum > target:
                    continue

                if len(new_sides) == dice_count:
                    if new_sides_sum == target:
                        fitting_permutations.append(new_sides)
                        print('Len fitting permutations :', len(fitting_permutations))
                        print('Fitting permutations:', fitting_permutations)
                    continue

                q.append(new_sides)

    return fitting_permutations



def probability(dice_number, sides, target):
    print('Dice number:', dice_number)
    print('Sides:      ', sides)
    print('Target:     ', target)

    permutations_count = sides ** dice_number
    print('Permutations count:  ', permutations_count)

    fitting_permutations = get_fitting_permutations(dice_number, sides, target)
    print('Fitting permutations:', fitting_permutations, len(fitting_permutations))

    target_probability = len(fitting_permutations) / permutations_count
    print('Target probability:  ', target_probability)
    print()
    return target_probability


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=4):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    # assert (almost_equal(probability(2, 6, 3), 0.0556)), "Basic example"
    # assert (almost_equal(probability(2, 6, 4), 0.0833)), "More points"
    # assert (almost_equal(probability(2, 6, 7), 0.1667)), "Maximum for two 6-sided dice"
    # assert (almost_equal(probability(2, 3, 5), 0.2222)), "Small dice"
    # assert (almost_equal(probability(2, 3, 7), 0.0000)), "Never!"
    # assert (almost_equal(probability(3, 6, 7), 0.0694)), "Three dice"
    assert (almost_equal(probability(10, 10, 50), 0.0375)), "Many dice, many sides"
