from itertools import product


def m_wins(o_dice, m_dice):
    o_score = 0
    for o_side, m_side in product(o_dice, m_dice):
        if o_side > m_side:
            o_score += 1
        elif o_side < m_side:
            o_score -= 1

    return o_score < 0


def get_mutated_dice(o_dice):
    o_dice_len = len(o_dice)
    o_dice_min = min(o_dice)
    o_dice_max = max(o_dice)
    o_dice_sum = sum(o_dice)

    m_dices = product(range(max(1, o_dice_min - 2), o_dice_max + 2), repeat=o_dice_len)

    m_dices_filtered = filter(lambda m_dice: sum(m_dice) == o_dice_sum, m_dices)

    yield from m_dices_filtered


def winning_die(enemy_die):
    tick = 0
    o_dice = enemy_die
    print('O dice:', o_dice)
    for mutated_dice in get_mutated_dice(o_dice):
        if tick > 10000:
            print('Tick limit:', tick)
            print()
            return []
        tick += 1
        if m_wins(o_dice, mutated_dice):
            print('Winning dice:', mutated_dice)
            print()
            return mutated_dice

    print('Unfortunately, no winning dice found')
    print()
    return []


if __name__ == '__main__':
    def check_solution(func, enemy):
        player = func(enemy)
        total = 0
        for p in player:
            for e in enemy:
                if p > e:
                    total += 1
                elif p < e:
                    total -= 1
        return total > 0


    assert check_solution(winning_die, [3, 3, 3, 3, 6, 6]), "Threes and Sixes"
    assert check_solution(winning_die, [4, 4, 4, 4, 4, 4]), "All Fours"
    assert check_solution(winning_die, [1, 1, 1, 4]), "Unities and Four"
    assert winning_die([1, 2, 3, 4, 5, 6]) == [], "All in row -- No die"

    assert check_solution(winning_die, [3, 3, 5, 6, 8, 9])  # == [1, 1, 3, 9, 10, 10]
    assert check_solution(winning_die, [3, 3, 5, 6, 7, 8, 9])  # == [1, 1, 1, 8, 10, 10, 10]
    assert check_solution(winning_die, [5, 6, 6, 8, 8, 10, 10, 10, 10])  # == [3, 3, 3, 9, 11, 11, 11, 11, 11]
    assert check_solution(winning_die, [1, 5, 5, 5, 5, 6, 6, 6, 6, 10])  # == [1, 1, 1, 1, 1, 7, 10, 11, 11, 11]
    assert winning_die([2, 4, 6, 8, 10, 12, 14, 16, 18]) == []
