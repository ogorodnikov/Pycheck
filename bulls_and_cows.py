from itertools import permutations

VARIANTS = set(permutations(range(10), 4))

def filter_variants(variants, result):

    for variant in variants:



def checkio(data):
    print('Data:', data)

    steps = [step.split(' ') for step in data]
    print('Steps:', steps)

    new_variants = VARIANTS

    for guess, result in steps:
        print('Guess:', guess)
        print('Result:', result)

        new_variants = filter_variants(new_variants, result)

        print('New variants:', new_variants)
        input()


    new_guess = next(iter(new_variants))
    new_guess_string = ''.join(map(str, guess))


    return guess_string

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
    # assert check_solution(checkio, "6130"), "6130"
    # assert check_solution(checkio, "0317"), "0317"
    # assert check_solution(checkio, "9876"), "9876"
