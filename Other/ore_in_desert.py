from itertools import product, starmap

BOARD_SIZE = 10
ALL_CELLS = set(starmap(complex, product(range(BOARD_SIZE), repeat=2)))


def checkio(previous):

    possible_cells = ALL_CELLS.copy()

    for center_y, center_x, radius in previous:

        center = complex(center_y, center_x)

        possible_cells &= {cell for cell in possible_cells
                           if radius + 0.5 >= abs(cell - center) >= radius - 0.5}

    next_cell = possible_cells.pop()
    next_cell_coordinates = int(next_cell.real), int(next_cell.imag)

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
    assert check_solution(checkio, (6, 6)), "Center"

    assert check_solution(checkio, (7, 8))
