import random

BOARD_SIZE = 10
board = {complex(y, x) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)}

possible_cells = board.copy()
last_step_cell = None


def print_board(cells):

    height = int(max(cell.real for cell in cells)) + 1
    width = int(max(cell.imag for cell in cells)) + 1

    print(''.join(map(str, range(width))))
    for y in range(height):
        row = ''
        for x in range(width):
            cell = complex(y, x)
            if cell in cells:
                row += 'X'
            else:
                row += '.'
        print(row)

def checkio(steps):

    current_step = steps[-1]
    print('Current step:', current_step)

    y, x, result = current_step
    step_cell = complex(y, x)
    print('Step cell:', step_cell)

    global possible_cells
    global last_step_cell

    print('Possible cells:', possible_cells)
    print('Last step cell:', last_step_cell)

    if result == 1:

        closer_cells = {cell for cell in board if abs(cell - step_cell) < abs(cell - last_step_cell)}
        possible_cells = closer_cells

        print('    Closer cells:', closer_cells)
        print('    Possible cells:', possible_cells)

    elif result == -1:

        further_cells = {cell for cell in board if abs(cell - step_cell) > abs(cell - last_step_cell)}
        possible_cells = further_cells

        print('    Further cells:', further_cells)
        print('    Possible cells:', possible_cells)

    print_board(possible_cells)

    last_step_cell = step_cell

    print('New Last step cell:', last_step_cell)

    # random_cell = random.choice(list(possible_cells))
    # print('Random cell:', random_cell)

    new_step_cell = step_cell - 2j
    print('New step cell:', new_step_cell)

    input()

    return new_step_cell.real, new_step_cell.imag

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
