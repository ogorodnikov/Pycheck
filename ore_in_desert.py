from itertools import product

BOARD_SIZE = 10
ALL_CELLS = {complex(y, x) for y, x in product(range(BOARD_SIZE), repeat=2)}


def checkio(previous):
    print('==== Previous:', previous)

    if not previous:
        return [BOARD_SIZE // 2, BOARD_SIZE // 2]

    possible_cells = ALL_CELLS.copy()

    for step in previous:
        print('Step:', step)

        center_y, center_x, radius = step
        center = complex(center_y, center_x)

        print('    Center:', center)
        print('    Radius:', radius)
        print('    Radius + 0.5:', radius + 0.5)
        print('    Radius - 0.5:', radius - 0.5)

        # for cell in ALL_CELLS:
        #     print(cell, abs(cell - center))
        #
        #
        #
        # quit()

        # print(abs((5 + 5j) - (1 + 1j)))
        # quit()

        possible_cells &= {cell for cell in ALL_CELLS
                           if radius + 0.5 >= abs(cell - center) >= radius - 0.5}

        possible_cells -= {center}

        print('Possible cells:', possible_cells)
        print()

    next_cell = possible_cells.pop()
    print('Next cell:', next_cell)

    next_cell_coordinates = int(next_cell.real), int(next_cell.imag)
    print('Next cell coordinates:', next_cell_coordinates)
    print()

    return next_cell_coordinates


if __name__ == '__main__':

    def check_solution(func, ore):
        recent_data = []
        for step in range(4):
            row, col = func([d[:] for d in recent_data])  # copy the list
            if row < 0 or row > 9 or col < 0 or col > 9:
                print("Where is our probe?")
                return False
            if (row, col) == ore:
                return True
            dist = round(((row - ore[0]) ** 2 + (col - ore[1]) ** 2) ** 0.5)
            recent_data.append([row, col, dist])
        print("It was the last probe.")
        return False

    assert check_solution(checkio, (1, 1)), "Example"
    assert check_solution(checkio, (9, 9)), "Bottom right"
    # assert check_solution(checkio, (6, 6)), "Center"
