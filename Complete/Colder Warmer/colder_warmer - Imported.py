def checkio(steps):
    print('Steps:', steps)
    print('Len steps :', len(steps))
    if len(steps) == 12:
        x = sum([x[2]+1 for x in steps[2:7]])
        print('X:', x)
        y = sum([x[2]+1 for x in steps[7:12]])
        print('Y:', y)
        print('[x if x < 10 else 9, y if y < 10 else 9]', [x if x < 10 else 9, y if y < 10 else 9])
        return [x if x < 10 else 9, y if y < 10 else 9]
    r = "0020406080909294969899"
    print('R:', r)
    print('2*len(steps)-2', 2*len(steps)-2)
    print('2*len(steps)-1', 2*len(steps)-1)
    print()
    return [int(r[2*len(steps)-2]), int(r[2*len(steps)-1])]


if __name__ == '__main__':

    from math import hypot

    MAX_STEP = 12


    def check_solution(func, goal, start):
        prev_steps = [start]
        for step in range(MAX_STEP):
            row, col = func([s[:] for s in prev_steps])
            if [row, col] == goal:
                return True
            if 10 <= row or 0 > row or 10 <= col or 0 > col:
                print("You gave wrong coordinates.")
                return False
            prev_distance = hypot(prev_steps[-1][0] - goal[0], prev_steps[-1][1] - goal[1])
            distance = hypot(row - goal[0], col - goal[1])
            alteration = 0 if prev_distance == distance else (1 if prev_distance > distance else -1)
            prev_steps.append([row, col, alteration])
        print("Too many steps")
        return False


    assert check_solution(checkio, [7, 7], [5, 5, 0]), "1st example"
    # assert check_solution(checkio, [5, 6], [0, 0, 0]), "2nd example"