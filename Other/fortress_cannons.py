from itertools import product
from functools import lru_cache

PATTERNS = {0: {'N': [(0, -1)],
                'NE': [(1, -1)],
                'SE': [(1, 0)],
                'S': [(0, 1)],
                'SW': [(-1, 0)],
                'NW': [(-1, -1)]},

            120: {'N': [(-1, -1), (1, -1)],
                  'NE': [(0, -1), (1, 0)],
                  'SE': [(1, -1), (0, 1)],
                  'S': [(-1, 0), (1, 0)],
                  'SW': [(-1, -1), (0, 1)],
                  'NW': [(-1, 0), (0, -1)]},

            60: {'N': [(-1, -2), (0, -1), (1, -2)],
                 'NE': [(1, -2), (1, -1), (2, 0)],
                 'SE': [(2, 0), (1, 0), (1, 1)],
                 'S': [(1, 1), (0, 1), (-1, 1)],
                 'SW': [(-1, 1), (-1, 0), (-2, 0)],
                 'NW': [(-2, 0), (-1, -1), (-1, -2)]}}

DIRECTIONS = ['N', 'NE', 'SE', 'S', 'SW', 'NW']

ALL_DIRECTIONS = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1)]

CLOCKWISE_EVEN = (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1)
CLOCKWISE_ODD = (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)

def print_hexagonal_grid(cells, mode='only'):
    start_row = 1
    end_row = 9

    start_column = 'A'
    end_column = 'L'

    n_columns = ord(end_column) - ord(start_column)

    print(r' ____     ' * (n_columns // 2 + 1))

    for i in range(start_row, end_row + 1):
        row_string1 = ''
        row_string2 = ''
        for j in range(0, n_columns, 2):
            column1 = chr(ord(start_column) + j)
            column2 = chr(ord(start_column) + j + 1)
            row = str(i)
            cell1 = column1 + row
            cell2 = column2 + row
            if mode == 'only':
                cell1 *= cell1 in cells
                cell2 *= cell2 in cells
            row_string1 += f'/ {cell1:2} \____'
            row_string2 += f'\____/ {cell2:2} '
        print(row_string1 + '/ ')
        print(row_string2 + '\ ')

    print(r'     \____' + r'/    \____' * (n_columns // 2) + '/')


@lru_cache(maxsize=1000)
def distance_bfs(cell1, cell2):
    checked = [cell1]
    q = [[cell1]]
    i = 0
    while q:
        a_cells = q.pop()
        b_cells = []
        i += 1
        for a in a_cells:
            ax = ord(a[0]) - 65
            ay = int(a[1:])
            if ax % 2:
                deltas = CLOCKWISE_ODD
            else:
                deltas = CLOCKWISE_EVEN
            for dx, dy in deltas:
                bx = ax + dx
                by = ay + dy
                b = chr(bx + 65) + str(by)
                if b == cell2:
                    return i
                if b not in checked:
                    b_cells.extend([b])
        checked.extend(b_cells)
        q.append(b_cells)


def fortress_cannons(fort, cannons, enemies):
    print('Fort:', fort)
    print('Cannons:')
    for cannon in cannons:
        print('   Angle: {}, Min: {}, Max: {}'.format(*cannon))
    print('Enemies:', *enemies)

    def propagate_pattern(position, pattern):
        # print('Propagating pattern:')
        # print('   Position:', position)
        # print('   Pattern:', pattern)

        sector_cells = []
        q = [position]
        while q:
            a = q.pop()
            ax = a[0]
            ay = int(a[1:])

            for destination in pattern:
                dx, dy = destination
                bx = ord(ax) + dx
                is_odd = bx % 2
                by = ay + dy + is_odd
                b = chr(bx) + str(by)
                if ord('L') >= bx >= ord('A') and 9 >= by >= 1 and b not in sector_cells:
                    # print('B:', b)
                    q.append(b)
                    sector_cells.append(b)

        return sector_cells

    def all_cells():
        return propagate_pattern('A1', ALL_DIRECTIONS)

    print()

    direction_list = []
    for i in range(len(cannons)):
        direction_list.append(DIRECTIONS)

    direction_variants = product(*direction_list)

    for cannon_directions in direction_variants:
        covered_cells = []
        for i, cannon in enumerate(cannons):
            angle, min_distance, max_distance = cannon
            direction = cannon_directions[i]
            sector_cells = propagate_pattern(fort, PATTERNS[angle][direction])
            sector_cells = [cell for cell in sector_cells if min_distance <= distance_bfs(fort, cell) <= max_distance]
            covered_cells.extend(sector_cells)

            print('Cannon:', i)
            print('   Angle: {}, Min: {}, Max: {}'.format(*cannon))
            print('Direction:', direction)
            print_hexagonal_grid(sector_cells)

        print('Total coverage for:', cannon_directions)
        print_hexagonal_grid(covered_cells)

        if all(enemy in covered_cells for enemy in enemies):
            print('All covered by directions combination:', list(cannon_directions))
            print('Enemies:', enemies)
            print('Covered cells:', covered_cells)
            print([enemy in covered_cells for enemy in enemies])

            return list(cannon_directions)

    return None


if __name__ == '__main__':
    assert fortress_cannons("D6", [[60, 2, 2], [60, 4, 4], [60, 6, 6], [60, 8, 8]], ["F5", "G4", "J4", "K2"]) == ['NE',
                                                                                                                  'NE',
                                                                                                                  'NE',
                                                                                                                  'NE']

    assert fortress_cannons('F5', [(0, 1, 4)], {'F2'}) == ['N'], '0 degree'
    assert fortress_cannons('F5', [(60, 1, 6)], {'K4'}) == ['NE'], '60 degree'
    assert fortress_cannons('F5', [(120, 1, 4)],{'B3', 'E8'}) == ['SW'], '120 degree'
    assert fortress_cannons('F5', [(0, 2, 6), (120, 1, 3), (60, 1, 4)], {'L2', 'D3', 'C6', 'E9'}) == ['NE', 'NW', 'S'], '3 cannons'
    assert fortress_cannons('F5', [(0, 1, 6), (120, 2, 3)], {'A3', 'E6', 'G7'}) is None, 'None'
