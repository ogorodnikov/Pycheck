from collections import defaultdict
from heapq import heappop, heappush

ACTION = ("L", "R", "F")
CHERRY = 'C'
OTHER_CHERRY = '*'
TREE = 'T'
SNAKE_HEAD = '0'
SNAKE = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
EMPTY = '.'
DIRECTIONS = {-1j: 'L', 1: 'F', -1: 'F', 1j: 'R'}
TICK_LIMIT = 10000


def field_map_to_dict(field_map):
    field_dict = defaultdict(set)

    for y, row in enumerate(field_map):
        for x, cell in enumerate(row):
            field_dict[cell].add(complex(x, y))

    return field_dict


def get_relative_direction(neck, head, neighbour):
    neck_delta = neck - head
    neighbour_delta = neighbour - head
    delta = neck_delta * neighbour_delta

    if neck_delta in (1, -1) and neighbour_delta in (1j, -1j):
        delta = delta.conjugate()

    direction = DIRECTIONS[delta]
    return direction


def get_head_neighbours(field, is_escape):
    head = field['0'].copy().pop()
    neck = field['1'].copy().pop()

    if is_escape:
        allowed_cells = field[EMPTY] | field[CHERRY] | field[OTHER_CHERRY]
    else:
        allowed_cells = field[EMPTY] | field[CHERRY]

    metrics = ((neighbour, get_relative_direction(neck, head, neighbour))
               for neighbour in allowed_cells
               if 0 < abs(neighbour - head) < 1.4)

    return metrics


def find_path(field, goal, is_escape=False):
    tick = 0
    q = [(0, tick, field, '')]
    while q:
        priority, _, field, path = heappop(q)

        # print('>>> Popping:')
        # print('Path:', path)
        # print_field(field)

        if tick >= TICK_LIMIT:
            print('    Tick limit reached:', tick)
            return None

        metrics = get_head_neighbours(field, is_escape=is_escape)
        for neighbour, direction in metrics:
            priority = abs(neighbour - goal) * len(path)
            new_field, tail = move_snake(field, neighbour, goal)

            new_path = path + direction

            # print('Neighbour:', neighbour)
            # print('New field:')
            # print_field(new_field)

            if neighbour == goal:

                if not is_escape:
                    print('    Proposed path:', new_path)
                    escape_path = find_path(new_field, tail.copy().pop(), is_escape=True)
                    if escape_path:
                        print('    Escape possible to:', tail.copy().pop())
                        print('    Escape path:', escape_path)
                        print('Path accepted:', new_path)
                    else:
                        print('    But no escape!')
                        continue

                return new_path

            tick += 1
            heappush(q, (priority, tick, new_field, new_path))


def move_snake(field, neighbour, goal):
    snake_cells = list(map(str, sorted(map(int, field.keys() & SNAKE))))
    snake_cells_without_head = snake_cells[1:]
    tail_index = max(map(int, snake_cells))
    tail = field[str(tail_index)]

    new_snake_without_head = list(zip(snake_cells_without_head,
                                      (field[cell]
                                       for cell in snake_cells)))
    new_head = [(SNAKE_HEAD, {neighbour})]
    new_snake = new_head + new_snake_without_head

    new_field = {key: value.copy() if isinstance(value, set)
    else value
                 for key, value in field.items()}

    new_field[EMPTY] -= {neighbour}
    new_field[EMPTY] |= tail
    new_field.update(new_snake)

    if neighbour == goal:
        # print('Expanding snake)')
        new_field[CHERRY] = set()
        new_field[EMPTY] -= tail
        new_field[str(tail_index + 1)] = tail

    return new_field, tail


def snake(field_map):
    print('New map:')
    print_map(field_map)

    field = field_map_to_dict(field_map)
    cherries = field[CHERRY]
    print('Cherries:', cherries)

    paths = []
    for cherry in cherries:
        print('Going for cherry:', cherry)
        other_cherries = cherries - {cherry}

        field[CHERRY] = {cherry}
        field[OTHER_CHERRY] = other_cherries

        path = find_path(field, cherry)
        paths.append(path)

    print('Paths:', paths)
    shortest_path = min(filter(None, paths), key=len)
    print('Shortest path:', shortest_path)
    print()
    return shortest_path


def print_map(field_map):
    map_height = len(field_map)
    map_width = len(field_map[0])
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y, row in enumerate(field_map):
        print(f'{y:{row_number_width}d} {row}')


def print_field(field):
    all_cells = {cell for key in field for cell in field[key]}

    field_width = int(max(cell.real for cell in all_cells)) + 1
    field_height = int(max(cell.imag for cell in all_cells)) + 1

    row_number_width = (field_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(field_width))

    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(field_height):
        row_string = ''.join(key for x in range(field_width)
                             for key in field
                             if complex(x, y) in field[key])
        print(f'{y:{row_number_width}d} {row_string}')


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


    # assert snake([".T.....T..",
    #               ".C........",
    #               ".....T....",
    #               "..T....T..",
    #               "..........",
    #               ".0...T....",
    #               ".1........",
    #               ".2.T...T..",
    #               ".3...T....",
    #               ".4........"]) == 'FFFF', "Single map"
    #
    # assert check_solution(snake, [
    #     ".T.....T..",
    #     ".C........",
    #     ".....T....",
    #     "..T....T..",
    #     "..........",
    #     ".0...T....",
    #     ".1........",
    #     ".2.T...T..",
    #     ".3...T....",
    #     ".4........"]), "Basic map"
    #
    # assert snake(["..T....T..",
    #               ".C.....T..",
    #               "...TTT....",
    #               "..T....T..",
    #               "..T...T6..",
    #               "..T.0T45..",
    #               "....123...",
    #               "...T..TT..",
    #               "....TT....",
    #               ".........."]), "1+j1"
    #
    # for _ in range(10):
    #     assert check_solution(snake, [
    #         "..T....T.C",
    #         ".......T..",
    #         "...TTT....",
    #         "..T....T..",
    #         "..T...T...",
    #         ".0T..T....",
    #         ".1........",
    #         ".2.T..TT..",
    #         ".3..TT....",
    #         ".4........"]), "Extra map"
    #
    # assert check_solution(snake, [
    #      ".T.....T..",
    #      ".C........",
    #      ".....T....",
    #      "..T....T..",
    #      "..........",
    #      ".0...T....",
    #      ".1...C....",
    #      ".2.T...T..",
    #      ".3...T....",
    #      ".4........"]), "Two cherries"

    for _ in range(1):
        assert check_solution(snake, ["..........",
                                      "..T.T.....",
                                      "..T.T.....",
                                      "..T.T.....",
                                      "..T.T.....",
                                      "..T.TTTTT.",
                                      "..TC......",
                                      "..TTTTTTT.",
                                      "..654321..",
                                      "..C....0.."]), "Extra 3"


# 0 ..........
# 1 ..T.T.....
# 2 ..T.T.....
# 3 ..TCT.....
# 4 ..T.T.....
# 5 ..T.TTTTT.
# 6 ..TC......
# 7 ..TTTTTTT.
# 8 ......76..
# 9 ..012345..