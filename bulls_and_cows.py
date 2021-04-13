from itertools import permutations

VARIANTS = set(''.join(map(str, permutation)) for permutation in permutations(range(10), 4))

def filter_variants(variants, guess, result):

    new_variants = set()

    for variant in variants:

        cow_count = 0
        bulls_count = 0

        # print('    Guess:  ', guess)
        # print('    Variant:', variant)

        for v, g in zip(variant, guess):
            # print('        V:', v)
            # print('        G:', g)

            if v == g:
                bulls_count += 1

            elif v in guess:
                cow_count += 1

        variant_result = f'{bulls_count}B{cow_count}C'
        # print('    Variant result:', variant_result)

        if variant_result == result:
            new_variants.add(variant)

    return new_variants




def checkio(data):
    print('Data:', data)

    steps = [step.split(' ') for step in data]
    print('Steps:', steps)

    new_variants = VARIANTS

    for guess, result in steps:
        print('Guess:', guess)
        print('Result:', result)

        new_variants = filter_variants(new_variants - {guess}, guess, result)

        print('New variants:', len(new_variants))

    new_guess = next(iter(new_variants))
    print('New guess:', new_guess)
    print()

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
