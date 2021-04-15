from itertools import permutations, starmap
from operator import eq

VARIANTS = set(''.join(map(str, permutation)) for permutation in permutations(range(10), 4))


def filter_variants(variants, guess, result):

    old_bull_count = int(result[0])
    old_cow_count = int(result[2])

    new_variants = set()

    for variant in variants - {guess}:

        bull_count = sum(starmap(eq, zip(variant, guess)))
        cow_count = len(set(guess) & set(variant)) - bull_count

        if bull_count == old_bull_count and cow_count == old_cow_count:
            new_variants.add(variant)

    return new_variants


def checkio(data):
    steps = [step.split(' ') for step in data]

    new_variants = VARIANTS

    for guess, result in steps:
        new_variants = filter_variants(new_variants, guess, result)

    new_guess = next(iter(new_variants))
    return new_guess

if __name__ == '__main__':

    def check_solution(func, goal):
        recent = []
        for step in range(8):
            user_result = func(recent)
            bulls = cows = 0
            for u, g in zip(user_result, goal):
                if u == g:
                    bulls += 1
                elif u in goal:
                    cows += 1
            recent.append("{0} {1}B{2}C".format(user_result, bulls, cows))
            if bulls == 4:
                print("{0} Win with {1} steps.".format(goal, step + 1))
                return True
        print("{0} Fail.".format(goal))
        return False

    assert check_solution(checkio, "1234"), "1234"
    assert check_solution(checkio, "6130"), "6130"
    assert check_solution(checkio, "0317"), "0317"
    assert check_solution(checkio, "9876"), "9876"
