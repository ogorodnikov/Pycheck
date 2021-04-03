# ACTIONS = (1, 0), (1, 2), (0, 1), (0, 2), (2, 1), (2, 0)
from itertools import product


def checkio(data):

    all_actions = list(filter(lambda pair: len(set(pair)) == 2, product((0, 1, 2), repeat=2)))

    start, end = data.split('-')

    min_actions_len = float('inf')
    start_registers = ['', start, '']
    history = [start_registers]

    q = [(start_registers, [])]

    while q:

        registers, actions = q.pop(0)

        for a, b in all_actions:

            print()
            print('Action:       ', (a, b))
            print('Registers:    ', registers)

            if not registers[a]:
                print('---- Register empty:', a)
                continue

            if b == 0 and len(registers[0]) == 1:
                print('---- Register 0 is full:', registers[0])
                continue

            new_actions = actions + [(a, b)]

            new_registers = registers.copy()

            letter = new_registers[a][-1]
            new_registers[a] = new_registers[a][:-1]
            new_registers[b] = new_registers[b] + letter

            print('New registers:', new_registers)

            if new_registers in history:
                print('---- Already in history')
                continue

            if new_registers[2] == end:
                print('    ==== End found:')
                print('         New registers:', new_registers)
                print('         New actions:', new_actions)
                min_actions_len = min(min_actions_len, len(new_actions))
                print('         New min actions len:', min_actions_len)
                continue

            if len(new_actions) == min_actions_len:
                continue

            q.append((new_registers, new_actions))
            history.append(new_registers)

    print('Q:', q)
    print('History:', history)
    print('Min actions len:', min_actions_len)
    quit()

    return ValueError


if __name__ == '__main__':
    GOOD_ACTIONS = ("12", "10", "01", "02", "20", "21")

    def check_solution(func, anagrams, min_length):
        start, end = anagrams.split("-")
        stacks = [[], list(start), []]
        user_result = func(anagrams)
        actions = user_result.split(",")
        user_actions = []
        for act in actions:
            if act not in GOOD_ACTIONS:
                print("Wrong action")
                return False
            from_s = int(act[0])
            to_s = int(act[1])
            if not stacks[from_s]:
                print("You can not get from an empty stack")
                return False
            if to_s == 0 and stacks[to_s]:
                print("You can not push in the full buffer")
                return False
            stacks[to_s].append(stacks[from_s].pop())
            user_actions.append(act)
        res_word = ''.join(stacks[2])
        if len(actions) > min_length:
            print("It can be shorter.")
            return False
        if res_word == end:
            return True
        else:
            print("The result anagram is wrong.")
            return False

    assert check_solution(checkio, "rice-cire", 5), "rice-cire"
    # assert check_solution(checkio, "tort-trot", 4), "tort-trot"
    # assert check_solution(checkio, "hello-holle", 14), "hello-holle"
    # assert check_solution(checkio, "anagram-mragana", 8), "anagram-mragana"
    # assert check_solution(checkio, "mirror-mirorr", 25), "mirror-mirorr"
