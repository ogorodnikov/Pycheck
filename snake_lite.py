from collections import defaultdict

ACTION = ("L", "R", "F")
CHERRY = 'C'
TREE = 'T'
SNAKE_HEAD = '0'
SNAKE = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
EMPTY = '.'
DIRECTIONS = {-1j: 'L', 1: 'F', -1: 'F', 1j: 'R'}


def print_map(field_map):
    map_height = len(field_map)
    map_width = len(field_map[0])
    row_number_width = (map_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(map_width))

    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y, row in enumerate(field_map):
        print(f'{y:{row_number_width}d} {row}')


def print_field(field):
    snake_cells = {field[snake_key].copy().pop() for snake_key in field.keys() & SNAKE}
    all_cells = field[EMPTY] | field[TREE] | field[CHERRY] | snake_cells

    field_width = int(max(cell.real for cell in all_cells)) + 1
    field_height = int(max(cell.imag for cell in all_cells)) + 1

    row_number_width = (field_height - 1) // 10 + 1
    column_numbers_string = ''.join(str(i % 10) for i in range(field_width))

    print(' ' + ' ' * row_number_width + column_numbers_string)
    for y in range(field_height):
        row_string = ''
        for x in range(field_width):
            for key in field:
                if isinstance(field[key], set) and complex(x, y) in field[key] or complex(x, y) == field[key]:
                    row_string += key
        print(f'{y:{row_number_width}d} {row_string}')


def field_map_to_dict(field_map):
    field_dict = defaultdict(set)

    for y, row in enumerate(field_map):
        for x, cell in enumerate(row):
            # if cell in SNAKE | {CHERRY}:
            #     field_dict[cell] = complex(x, y)
            #     continue
            field_dict[cell].add(complex(x, y))

    return field_dict


def find_step_to_cherry(field):
    head = field['0'].copy().pop()
    neck = field['1'].copy().pop()
    cherry = field['C'].copy().pop()

    distances, neighbours = zip(*((abs(neighbour - cherry), neighbour)
                                  for neighbour in field[EMPTY] | {cherry}
                                  if abs(neighbour - head) < 1.4))

    closest_neighbours = [n for d, n in zip(distances, neighbours) if d == min(distances)]
    random_closest_neighbour = choice(closest_neighbours)

    print('Closest neighbours:', closest_neighbours)
    print('Random closest neighbour:', random_closest_neighbour)

    next_step_direction = get_relative_direction(neck, head, random_closest_neighbour)
    return next_step_direction


def get_relative_direction(neck, head, neighbour):
    neck_delta = neck - head
    neighbour_delta = neighbour - head
    delta = neck_delta * neighbour_delta

    if neck_delta in (1, -1) and neighbour_delta in (1j, -1j):
        delta = delta.conjugate()

    direction = DIRECTIONS[delta]
    return direction


def get_head_neighbours(field):
    head = field['0'].copy().pop()
    neck = field['1'].copy().pop()
    cherry = field['C'].copy().pop()

    metrics = ((abs(neighbour - cherry),
                neighbour,
                get_relative_direction(neck, head, neighbour))
               for neighbour in field[EMPTY] | {cherry}
               if abs(neighbour - head) < 1.4)

    return metrics


def find_path(field, goal):
    q = [(field, '')]
    while q:
        field, path = q.pop(0)

        metrics = get_head_neighbours(field)
        for distance, neighbour, direction in metrics:
            print('Neighbour:', neighbour)
            print('Distance: ', distance)
            print('Direction:', direction)

            new_field = move_snake(field, neighbour)
            print('New field:')
            print_field(new_field)

            new_path = path + direction

            if {neighbour} == goal:
                print('Goal reached ============================================')
                return new_path

            q.append((new_field, new_path))


def move_snake(field, neighbour):
    snake_cells = sorted(field.keys() & SNAKE)
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

    cherry = new_field[CHERRY].copy().pop()
    if cherry == neighbour:
        print('Eating')
        new_field[CHERRY] = set()
        new_field[EMPTY] -= tail
        new_field[str(tail_index + 1)] = tail

    return new_field


def snake(field_map):
    print_map(field_map)

    field = field_map_to_dict(field_map)

    next_step = find_step_to_cherry(field)
    print('Next step:', next_step)
    print()

    path = find_path(field, field['C'])
    print('Path:', path)
    print()

    return path


if __name__ == '__main__':
    from random import randint, choice


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


    snake([".T.....T..",
           ".C........",
           ".....T....",
           "..T....T..",
           "..........",
           ".0...T....",
           ".1........",
           ".2.T...T..",
           ".3...T....",
           ".4........"])

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

    # assert check_solution(snake, [
    #     "..T....T.C",
    #     ".......T..",
    #     "...TTT....",
    #     "..T....T..",
    #     "..T...T...",
    #     ".0T..T....",
    #     ".1........",
    #     ".2.T..TT..",
    #     ".3..TT....",
    #     ".4........"]), "Extra map"
