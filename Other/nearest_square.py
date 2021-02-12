def nearest_square(number):
    print('Number:', number)
    previous_number = number - 1
    next_number = number + 1
    while True:
        print('Previous number:', previous_number)
        print('Next number:', next_number)
        if round(previous_number ** 0.5) == previous_number ** 0.5:
            print('=== Result:', previous_number)
            return previous_number
        elif round(next_number ** 0.5) == next_number ** 0.5:
            print('=== Result:', next_number)
            return next_number
        previous_number -= 1
        next_number += 1


if __name__ == '__main__':
    assert nearest_square(8) == 9
    assert nearest_square(13) == 16
    assert nearest_square(24) == 25
    assert nearest_square(9876) == 9801
    print("Coding complete? Click 'Check' to earn cool rewards!")
