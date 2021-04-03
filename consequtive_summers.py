def count_consecutive_summers(num):

    match_counter = 0

    for start in range(1, num + 1):
        for end in range(start, num + 1):

            range_sum = sum(range(start, end + 1))

            if range_sum == num:
                match_counter += 1

            if range_sum >= num:
                break

    print('Number:       ', num)
    print('Match counter:', match_counter)

    return match_counter


if __name__ == '__main__':
    assert count_consecutive_summers(42) == 4

    assert count_consecutive_summers(99) == 6
    assert count_consecutive_summers(1) == 1

    assert count_consecutive_summers(2835) == 20
