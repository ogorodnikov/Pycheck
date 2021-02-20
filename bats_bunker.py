from cmath import phase, polar, sin, pi, tau
from collections import defaultdict
from itertools import product, permutations
from typing import List

BAT = 'B'
ALPHA_BAT = 'A'
WALL = 'W'
EMPTY = '-'
CAVE_ENTRANCE = (0 + 0j)


def map_to_field(bunker_map):
    field = defaultdict(list)
    for y, row in enumerate(bunker_map):
        for x, cell in enumerate(row):
            field[cell].append(complex(x, y))
    return field


def check_connection(bat_a, bat_b, wall):
    print('Bat a:', bat_a)
    print('Bat b:', bat_b)
    print('--- Wall:', wall)

    wall_corners = [wall + complex(*delta) for delta in product((-0.5, 0.5), repeat=2)]
    print('    Wall corners:', wall_corners)

    bat_a_to_corners_vectors = [wall_corner - bat_a for wall_corner in wall_corners]
    print('    Bat a to wall corners vectors:', bat_a_to_corners_vectors)

    angles = [phase(vector) for vector in bat_a_to_corners_vectors]
    print('    Angles:', angles)

    min_angle = min(angles) % tau
    max_angle = max(angles) % tau
    print('    Min angle:', min_angle)
    print('    Max angle:', max_angle)

    bat_a_to_b_angle = phase(bat_b - bat_a) % tau
    print('    Bat a to b angle:', bat_a_to_b_angle)

    bat_a_to_wall_distance = abs(wall - bat_a)
    print('    Bat a to wall distance:', bat_a_to_wall_distance)

    bat_a_to_bat_b_distance = abs(bat_b - bat_a)
    print('    Bat a to bat b distance:', bat_a_to_bat_b_distance)

    wall_is_closer_then_bat_b = bat_a_to_wall_distance < bat_a_to_bat_b_distance
    print('    Wall is closer then bat b:', wall_is_closer_then_bat_b)

    is_in_sector = min_angle <= bat_a_to_b_angle <= max_angle
    print('    Is in sector:', is_in_sector)
    is_connected = not (is_in_sector and wall_is_closer_then_bat_b)

    print('Is connected:', is_connected)
    print()
    return is_connected


def find_shortest_path(start, goal, connections):
    print('Start:', start)

    if start == goal:
        return 0

    distances = []
    for neighbour in connections[start]:
        print('    Neighbour:', neighbour)

        distance = abs(neighbour - start)
        print('        Distance:', distance)

        if neighbour == goal:
            print('        === Goal found, returning distance:', distance)
            return distance

        new_connections = {key: {e for e in value} for key, value in connections.items()}
        new_connections[start] -= {neighbour}
        new_connections[neighbour] -= {start}
        print('        New connections:', new_connections)

        neighbour_to_goal_distance = find_shortest_path(neighbour, goal, new_connections)
        print('        Neighbour to goal distance:', neighbour_to_goal_distance)

        total_distance = distance + neighbour_to_goal_distance
        print('        Total distance:', total_distance)

        distances.append(total_distance)

    print('Distances from', start, ':', distances)

    if not distances:
        return float('inf')

    min_distance = min(distances)
    print('Min distance from', start, ':', min_distance)
    print()
    return min_distance


def checkio(bunker: List[str]) -> [int, float]:
    print('Bunker:')
    [print(row) for row in bunker]

    field = map_to_field(bunker)
    print('Field:', field)

    all_bats = field[BAT] + field[ALPHA_BAT]
    print('All bats:', all_bats)
    print()

    bat_connections = defaultdict(set)
    for bat_a, bat_b in permutations(all_bats, 2):
        if all(check_connection(bat_a, bat_b, wall) for wall in field[WALL]):
            print(bat_a, 'is connected with', bat_b)
            bat_connections[bat_a] |= {bat_b}
        else:
            print(bat_a, 'is not connected with', bat_b)

    print('Bat connections:')
    for bat, connections in bat_connections.items():
        print(f'{bat:7}: {connections}')
    print()

    shortest_path = find_shortest_path(CAVE_ENTRANCE, field[ALPHA_BAT].copy().pop(), bat_connections)
    print('Shortest path:', shortest_path)
    print()

    # n = 16
    # for angle in (1j ** (i / n * 4) for i in range(n + 1)):
    #     print('Phase:', phase(angle))
    #     print('Polar:', polar(angle))
    #     print('Phase angle 2 pi:', phase(angle) % tau)
    #     print()

    return shortest_path


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=2):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    # assert almost_equal(checkio([
    #     "B--",
    #     "---",
    #     "--A"]), 2.83), "1st example"
    #
    # assert almost_equal(checkio([
    #     "B-B",
    #     "BW-",
    #     "-BA"]), 4), "2nd example"

    # assert almost_equal(checkio([
    #     "B--",
    #     "-BA",
    #     "--W"]), 2.24)

    assert almost_equal(checkio([
        "BWA"]), float('inf'))

    # assert almost_equal(checkio([
    #     "BWB--B",
    #     "-W-WW-",
    #     "B-BWAB"]), 12), "3rd example"

    # assert almost_equal(checkio([
    #     "B---B-",
    #     "-WWW-B",
    #     "-WA--B",
    #     "-W-B--",
    #     "-WWW-B",
    #     "B-BWB-"]), 9.24), "4th example"
