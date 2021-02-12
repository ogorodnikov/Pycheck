import itertools

# Imported 1
# def find_min_difference(data):
#     print('Data:', data)
#
#     differences = {0}
#     for weight in data:
#         print('Weight:', weight)
#         new_differences = set()
#         for difference in differences:
#             new_differences.add(abs(weight - difference))
#             new_differences.add(abs(weight + difference))
#         differences = new_differences
#         print('Differences:', differences)
#
#     print('Minimum difference:', min(differences))
#     print()
#     return min(differences)


# Imported 2
def checkio(data):
    print('Data:', data)
    min_difference = mass = sum(data)
    print('Mass:', mass)
    for combination in itertools.product((0, 1), repeat=len(data)):
        print('Combination:', combination)
        print(*itertools.compress(data, combination))
        min_difference = min(min_difference, abs(mass - 2 * sum(itertools.compress(data, combination))))
        print('Min difference:', min_difference)
        print()

    print('Final min difference:', min_difference)
    print()
    print(*itertools.product((0, 1, 5), repeat=4))

    return min_difference


if __name__ == '__main__':
    # assert checkio([10, 10]) == 0, "1st example"
    # assert checkio([10]) == 10, "2nd example"
    assert checkio([5, 8, 13, 27, 14]) == 3, "3rd example"
    # assert checkio([5, 5, 6, 5]) == 1, "4th example"
    # assert checkio([12, 30, 30, 32, 42, 49]) == 9, "5th example"
    # assert checkio([1, 1, 1, 3]) == 0, "6th example"
