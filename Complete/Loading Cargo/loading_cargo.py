from itertools import permutations


def checkio(data):
    print('Data:', data)

    min_difference = float('INF')

    for weights_combination in permutations(data, len(data)):
        print('Weights combination:', weights_combination)
        for border_index in range(len(data)):
            left = weights_combination[:border_index]
            right = weights_combination[border_index:]
            print('    Pair:', (left, right))
            left_weight = sum(left)
            right_weight = sum(right)
            print('    Weights:', (left_weight, right_weight))
            weight_difference = abs(left_weight - right_weight)
            print('        Weight difference:', weight_difference)
            min_difference = min(min_difference, weight_difference)
            print('        Min difference:', min_difference)

    print('Final minimum difference:', min_difference)
    print()
    return min_difference


if __name__ == '__main__':
    assert checkio([10, 10]) == 0, "1st example"
    assert checkio([10]) == 10, "2nd example"
    assert checkio([5, 8, 13, 27, 14]) == 3, "3rd example"
    assert checkio([5, 5, 6, 5]) == 1, "4th example"
    assert checkio([12, 30, 30, 32, 42, 49]) == 9, "5th example"
    assert checkio([1, 1, 1, 3]) == 0, "6th example"
