ACTION = ("L", "R", "F")
CHERRY = 'C'
TREE = 'T'
SNAKE_HEAD = '0'
SNAKE = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
EMPTY = "."


def snake(field_map):
    return "F" or "R" or "L" or "FRL"


if __name__ == '__main__':
    from random import randint

    def find_snake(field_map):
        snake = {}
        for i, row in enumerate(field_map):
            for j, ch in enumerate(row):
                if ch in SNAKE:
                    snake[ch] = (i, j)
        return snake

    def find_new_head(snake, action):
        head = snake[SNAKE_HEAD]
        snake_dir = (head[0] - snake["1"][0], head[1] - snake["1"][1])
        if action == 'F':
            return head[0] + snake_dir[0], head[1] + snake_dir[1]
        elif action == 'L':
            return head[0] - snake_dir[1], head[1] + snake_dir[0]
        elif action == 'R':
            return head[0] + snake_dir[1], head[1] - snake_dir[0]
        else:
            raise ValueError("The action must be only L,R or F")

    def pack_map(list_map):
        return [''.join(row) for row in list_map]

    def check_solution(func, field_map):
        temp_map = [list(row) for row in field_map]
        step_count = 250
        while True:
            route = func(field_map[:])
            res_route = ""
            for ch in route:
                if step_count < 0:
                    print("Too many steps (no more than 250)."),
                    return False
                if ch not in ACTION:
                    print("The route must contain only F,L,R symbols")
                    return False
                res_route += ch
                snake = find_snake(temp_map)
                tail = snake[max(snake.keys())]
                temp_map[tail[0]][tail[1]] = EMPTY
                new_head = find_new_head(snake, ch)
                for s_key in sorted(snake.keys())[:-1]:
                    s = snake[s_key]
                    temp_map[s[0]][s[1]] = str(int(temp_map[s[0]][s[1]]) + 1)
                if (new_head[0] < 0 or new_head[0] >= len(temp_map) or
                        new_head[1] < 0 or new_head[1] >= len(temp_map[0])):
                    print("The snake crawl outside")
                    return False
                elif temp_map[new_head[0]][new_head[1]] == 'T':
                    print("The snake struck at the tree")
                    return False
                elif temp_map[new_head[0]][new_head[1]] in SNAKE:
                    print("The snake bit itself")
                    return False

                if temp_map[new_head[0]][new_head[1]] == 'C':
                    temp_map[new_head[0]][new_head[1]] = SNAKE_HEAD
                    if max(snake.keys()) == '9':
                        return True
                    else:
                        temp_map[tail[0]][tail[1]] = str(int(max(snake.keys())) + 1)
                        cherry = (randint(1, len(temp_map) - 2),
                                  randint(1, len(temp_map[0]) - 2))
                        while temp_map[cherry[0]][cherry[1]] != EMPTY:
                            cherry = (randint(1, len(temp_map) - 2),
                                      randint(1, len(temp_map[0]) - 2))
                        temp_map[cherry[0]][cherry[1]] = CHERRY
                        step_count -= 1
                else:
                    temp_map[new_head[0]][new_head[1]] = SNAKE_HEAD
                step_count -= 1
                field_map = pack_map(temp_map)

    assert check_solution(snake, [
        ".T.....T..",
        ".C........",
        ".....T....",
        "..T....T..",
        "..........",
        ".0...T....",
        ".1........",
        ".2.T...T..",
        ".3...T....",
        ".4........"]), "Basic map"
    assert check_solution(snake, [
        "..T....T.C",
        ".......T..",
        "...TTT....",
        "..T....T..",
        "..T...T...",
        ".0T..T....",
        ".1........",
        ".2.T..TT..",
        ".3..TT....",
        ".4........"]), "Extra map"