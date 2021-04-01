def checkio(data):

    start, end = data.split('-')

    start_parts = (start, '', '')

    min_actions_len = float('inf')
    history = {start_parts}
    q = [(start_parts, [])]

    while q:
        (a, b, c), actions = q.pop()

        if a:
            a1 = a[:-1]
            b1 = b + a[-1]
            c1 = c

            action = '10'

            new_parts = (a1, b1, c1)

            if new_parts[2] == end:
                new_actions = actions + [action]
                new_actions_len = len(actions + [action])
                print('New parts:', new_parts)
                print('Actions:', new_actions, new_actions_len)

                if new_actions_len < min_actions_len:
                    print('++++ New min length:', new_actions_len)
                    min_actions_len = new_actions_len


                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

            a2 = a[:-1]
            b2 = b
            c2 = c + a[-1]

            action = '12'

            new_parts = (a2, b2, c2)

            if new_parts[2] == end:
                print('New parts:', new_parts)
                print('Actions:', actions + [action], len(actions + [action]))
                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

        if b:
            b1 = b[:-1]
            a1 = a + b[-1]
            c1 = c

            action = '01'

            new_parts = (a1, b1, c1)

            if new_parts[2] == end:
                print('New parts:', new_parts)
                print('Actions:', actions + [action], len(actions + [action]))
                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

            b2 = b[:-1]
            a2 = a
            c2 = c + b[-1]

            action = '02'

            new_parts = (a2, b2, c2)

            if new_parts[2] == end:
                print('New parts:', new_parts)
                print('Actions:', actions + [action], len(actions + [action]))
                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

        if c:
            c1 = c[:-1]
            a1 = a + c[-1]
            b1 = b

            action = '21'

            new_parts = (a1, b1, c1)

            if new_parts[2] == end:
                print('New parts:', new_parts)
                print('Actions:', actions + [action], len(actions + [action]))
                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

            c2 = c[:-1]
            a2 = a
            b2 = b + c[-1]

            action = '20'

            new_parts = (a2, b2, c2)

            if new_parts[2] == end:
                print('New parts:', new_parts)
                print('Actions:', actions + [action], len(actions + [action]))
                quit()
            if new_parts not in history:
                q.append((new_parts, actions + [action]))
                history.add(new_parts)

        print('Q:', q)
        print('History:', history)
        print()

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
