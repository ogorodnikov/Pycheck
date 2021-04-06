BOARD_SIZE = 10

possible_cells = {complex(y, x) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)}
previous_cell = None


def closer_cells(closer_cell, further_cell):
    return {cell for cell in possible_cells
            if abs(cell - closer_cell) < abs(cell - further_cell)}


def checkio(steps):
    global possible_cells
    global previous_cell

    y, x, result = steps[-1]
    current_cell = complex(y, x)

    possible_cells -= {current_cell}

    if result == 1:
        possible_cells &= closer_cells(current_cell, previous_cell)

    elif result == -1:
        possible_cells &= closer_cells(previous_cell, current_cell)

    next_step = min(possible_cells,
                    key=lambda new_cell: abs(
                        len(closer_cells(new_cell, current_cell)) -
                        len(closer_cells(current_cell, new_cell))))

    previous_cell = current_cell

    print_possible_cells()
    print('Next step:', next_step)

    next_step_coordinates = list(map(int, (next_step.real, next_step.imag)))
    return next_step_coordinates


def print_possible_cells():
    height = int(max(cell.real for cell in possible_cells)) + 1
    width = int(max(cell.imag for cell in possible_cells)) + 1

    print(''.join(map(str, range(width))))
    for y in range(height):
        row = ''.join('X' if complex(y, x) in possible_cells else '.'
                      for x in range(width))
        print(row)



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
