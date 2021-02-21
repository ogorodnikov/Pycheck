from cmath import phase, pi, tau
from collections import defaultdict
from itertools import product, permutations
from timeit import timeit
from typing import List

BAT = 'B'
ALPHA_BAT = 'A'
WALL = 'W'
EMPTY = '-'
CAVE_ENTRANCE = (0 + 0j)
DELTAS = (0.5 - 0.5j), (-0.5 - 0.5j), (-0.5 + 0.5j), (+0.5 + 0.5j)

tick = 0
min_path_len = float('inf')


def map_to_field(bunker_map):
    field = defaultdict(list)
    for y, row in enumerate(bunker_map):
        for x, cell in enumerate(row):
            field[cell].append(complex(x, y))
    return field


def get_bat_connections(field):
    all_bats = field[BAT] + field[ALPHA_BAT]
    # print('All bats:', all_bats)
    # print()

    bat_connections = defaultdict(set)
    for bat_a, bat_b in permutations(all_bats, 2):
        # print('Bat a:', bat_a)
        # print('Bat b:', bat_b)
        if all(check_connection(bat_a, bat_b, wall) for wall in field[WALL]):
            # print('=== Connected:', bat_a, bat_b)
            # print()
            bat_connections[bat_a] |= {bat_b}
        else:
            # print('=== Not connected:', bat_a, bat_b)
            # print()
            pass

    return bat_connections


def check_connection(bat_a, bat_b, wall):
    # print('--- Wall:                         ', wall)

    wall_corners = [wall + delta for delta in DELTAS]
    # print('    Wall corners:                 ', wall_corners)

    bat_a_to_corners_vectors = [wall_corner - bat_a for wall_corner in wall_corners]
    # print('    Bat a to wall corners vectors:', bat_a_to_corners_vectors)

    angles = [phase(vector.conjugate()) % tau for vector in bat_a_to_corners_vectors]
    # print('    Angles:                       ', angles)

    min_angle = min(angles)
    max_angle = max(angles)
    # print('    Min angle:                    ', min_angle)
    # print('    Max angle:                    ', max_angle)

    angle_delta = max_angle - min_angle
    # print('    Angle delta:                  ', angle_delta)

    bat_a_to_b_vector = bat_b - bat_a
    # print('    Bat a to b vector:            ', bat_a_to_b_vector)

    bat_a_to_b_angle_without_tau = phase(bat_a_to_b_vector.conjugate())
    # print('    Bat a to b angle without tau: ', bat_a_to_b_angle_without_tau)

    bat_a_to_b_angle = phase(bat_a_to_b_vector.conjugate()) % tau
    # print('    Bat a to b angle:             ', bat_a_to_b_angle)

    if angle_delta >= pi:
        # print('        Angle delta >= pi')
        recalculated_angles = [phase(vector.conjugate()) for vector in bat_a_to_corners_vectors]
        # print('        Recalculated angles:      ', recalculated_angles)

        recalculated_min_angle = min(recalculated_angles)
        recalculated_max_angle = max(recalculated_angles)
        # print('        Recalculated min angle:   ', recalculated_min_angle)
        # print('        Recalculated max angle:   ', recalculated_max_angle)

        is_in_sector = recalculated_min_angle <= bat_a_to_b_angle_without_tau <= recalculated_max_angle
        # print('        Is in sector:             ', is_in_sector)

    else:
        is_in_sector = min_angle <= bat_a_to_b_angle <= max_angle
        # print('    Is in sector:                 ', is_in_sector)

    bat_a_to_wall_distance = abs(wall - bat_a)
    # print('    Bat a to wall distance:       ', bat_a_to_wall_distance)

    bat_a_to_bat_b_distance = abs(bat_b - bat_a)
    # print('    Bat a to bat b distance:      ', bat_a_to_bat_b_distance)

    wall_is_closer_then_bat_b = bat_a_to_wall_distance < bat_a_to_bat_b_distance
    # print('    Wall is closer then bat b:    ', wall_is_closer_then_bat_b)

    is_connected = not (is_in_sector and wall_is_closer_then_bat_b)

    # print('Is connected:', is_connected)
    # print()
    return is_connected


def find_shortest_path(start, goal, connections, path_len=0, level=0):
    global tick, min_path_len
    print('Tick:', tick)
    print('Start:', start)
    print('Level:', level)
    print('Min path length:', min_path_len)

    if start == goal:
        return 0

    distances = []
    for neighbour in connections[start]:
        print('    Neighbour:', neighbour)

        distance = abs(neighbour - start)
        print('        Distance:', distance)

        new_path_len = path_len + distance
        print('        New path len:', new_path_len)

        if new_path_len >= min_path_len:
            print('        --- New path len reached already found minimum:', min_path_len)
            continue

        if neighbour == goal:
            print('        >>> Goal found')
            print('        Distance:', distance)
            print('        New path len:', new_path_len)

            if new_path_len < min_path_len:
                min_path_len = new_path_len
                print('        +++ New Min path len', min_path_len)

            return distance

        new_connections = {key: {e for e in value} for key, value in connections.items()}
        new_connections[start] -= {neighbour}
        new_connections[neighbour] -= {start}
        # print('        New connections:', new_connections)

        tick += 1

        neighbour_to_goal_distance = find_shortest_path(neighbour, goal, new_connections, new_path_len, level + 1)
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
    global min_path_len
    min_path_len = float('inf')

    field = map_to_field(bunker)

    bat_connections = get_bat_connections(field)

    print('Bunker:')
    [print(row) for row in bunker]
    print()

    print('Bat connections:')
    for bat, connections in bat_connections.items():
        print(f'{bat:7}: {connections}')
    print()

    shortest_path = find_shortest_path(CAVE_ENTRANCE, field[ALPHA_BAT].copy().pop(), bat_connections)

    print('Shortest path:', shortest_path)
    print()
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
    #
    # assert almost_equal(checkio([
    #     "BWB--B",
    #     "-W-WW-",
    #     "B-BWAB"]), 12), "3rd example"

    assert almost_equal(checkio([
        "B---B-",
        "-WWW-B",
        "-WA--B",
        "-W-B--",
        "-WWW-B",
        "B-BWB-"]), 9.24), "4th example"

    # assert almost_equal(checkio([
    #     "B-B--B-",
    #     "-W-W-W-",
    #     "--B---B",
    #     "BW-W-W-",
    #     "----A--",
    #     "BW-W-W-",
    #     "-B--B-B"]), 16), "Extra 5"

    # print(timeit(lambda: almost_equal(checkio([
    #     "B-B--B-B-B--B-",
    #     "-W-W-W--W-W-W-",
    #     "--B---B--B---B",
    #     "BW-W-W-BW-W-W-",
    #     "----W------A--",
    #     "BW-W-W-BW-W-W-",
    #     "-B--B-B-B--B-B"]), 16), number=1))

    ### Line tests

    # assert almost_equal(checkio([
    #     "BWA"]), float('inf'))

    # assert almost_equal(checkio([
    #     "B",
    #     "W",
    #     "A"]), float('inf'))

    # assert almost_equal(checkio([
    #       "--B",
    #       "-W-",
    #       "A--"]), float('inf'))
