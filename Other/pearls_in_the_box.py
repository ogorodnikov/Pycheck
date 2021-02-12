def checkio(marbles: str, step: int) -> float:
    print('Marbles:', marbles)
    print('Step count:', step)

    w_probability_final = 0
    marbles_len = len(marbles)

    q = [(marbles, 1, 1)]
    while q:
        pearls, level, branch_probability = q.pop()

        if level > step:
            continue
        elif level == step:
            w_probability = branch_probability * pearls.count('w') / marbles_len
            w_probability_final += w_probability
            print('Adding W probability:', w_probability)
            continue

        for take_pearl in set(pearls):
            put_pearl = 'bw'.replace(take_pearl, '')
            new_pearls = pearls.replace(take_pearl, put_pearl, 1)
            take_probability = pearls.count(take_pearl) / marbles_len
            full_probability = branch_probability * take_probability

            print('Level:', level + 1)
            print('    New pearls:        ', new_pearls)
            print('    Branch probability:', branch_probability)
            print('    Take probability:  ', take_probability)
            print('    Full probability:  ', full_probability)

            q.append((new_pearls, level + 1, full_probability))

    final_rounded_w_probability = round(w_probability_final, 2)
    print('Final rounded w probability:', final_rounded_w_probability)
    print()
    return final_rounded_w_probability


if __name__ == '__main__':
    assert checkio('bbw', 3) == 0.48, "1st example"
    assert checkio('wwb', 3) == 0.52, "2nd example"
    assert checkio('www', 3) == 0.56, "3rd example"
    assert checkio('bbbb', 1) == 0, "4th example"
    assert checkio('wwbb', 4) == 0.5, "5th example"
    assert checkio('bwbwbwb', 5) == 0.48, "6th example"
    assert checkio("w", 1) == 1

    assert checkio("wwwwwbwbwbbwbbwwbw", 11) == 0.53
