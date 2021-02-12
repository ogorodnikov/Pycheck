from itertools import product

def lanterns_flow(river_map, minutes):
    print('Minutes:', minutes)
    river_width = river_map[0].count('.')
    map_width = len(river_map[0])
    map_length = len(river_map)
    rivers = []
    lightened_cells = set()
    new_map = [[e for e in row] for row in river_map]

    # mark river cells
    for i in range(river_width):
        rivers.append([])
        q = [(0, 0)]
        checked = set()
        river_name = str(i)
        while q:
            a, b = q.pop()
            checked.add((a, b))
            for da, db in product(range(-1, 2), range(-1, 2)):
                x = a + da
                y = b + db
                if 0 <= x < map_width and 0 <= y < map_length:
                    if new_map[y][x] == '.':
                        new_map[y][x] = river_name
                        rivers[i].append((x, y))
                    elif (x, y) not in checked and new_map[y][x] != river_name:
                        q.append((x, y))

        # go down the river
        time = 0
        x, y = new_map[0].index(river_name), 0
        checked = {(x, y)}
        is_changed = True
        while is_changed:
            # gather lightened cells
            if time == minutes:
                for dx, dy in product(range(-1, 2), range(-1, 2)):
                    lightened_x = x + dx
                    lightened_y = y + dy
                    if 0 <= lightened_x < map_width and 0 <= lightened_y < map_length:
                        if new_map[lightened_y][lightened_x] != 'X':
                            lightened_cells.add((lightened_x, lightened_y))
                break

            # find next river cell
            is_changed = False
            for dx, dy in (0, -1), (1, 0), (0, 1), (-1, 0):
                next_x = x + dx
                next_y = y + dy
                if 0 <= next_x < map_width and 0 <= next_y < map_length:
                    if new_map[next_y][next_x] == river_name and (next_x, next_y) not in checked:
                        x, y = next_x, next_y
                        checked.add((x, y))
                        is_changed = True
                        time += 1
                        break

    print('River cells:')
    for river_cells in rivers:
        print(*river_cells)

    print('New map:')
    for row in new_map:
        print(*row)

    print('Lightened cells:', *sorted(lightened_cells))
    lightened_area = len(lightened_cells)

    print('Lightened area:', lightened_area)
    print()
    return lightened_area


if __name__ == '__main__':
    assert lanterns_flow(("X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X......X",
                          "X......X",
                          "X......X",
                          "X......X",
                          "XXX....X"), 7) == 18, "7th minute"
    assert lanterns_flow(("X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X......X",
                          "X......X",
                          "X......X",
                          "X......X",
                          "XXX....X"), 0) == 8, "Start"
    assert lanterns_flow(("X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X....XXX",
                          "X......X",
                          "X......X",
                          "X......X",
                          "X......X",
                          "XXX....X"), 9) == 17, "9th minute"
    assert lanterns_flow(("X.XX",
                          "X..X",
                          "XX.X",
                          "X..X",
                          "X.XX"), 3) == 5, "Extra 2"
    assert lanterns_flow(("X..XXXXXXX",
                          "X..X.....X",
                          "X..X.....X",
                          "X.....X..X",
                          "X.....X..X",
                          "XXXXXXX..X",
                          "XX.......X",
                          "XX.......X",
                          "XX..XXXXXX"), 4) == 10, "Extra 4"
