def checkio(data):
    return ""


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
