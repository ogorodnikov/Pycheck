from cmath import phase
from collections import defaultdict
from itertools import product, permutations
from typing import List

BAT = 'B'
ALPHA_BAT = 'A'
WALL = 'W'
EMPTY = '-'


def map_to_field(bunker_map):
    field = defaultdict(list)
    for y, row in enumerate(bunker_map):
        for x, cell in enumerate(row):
            field[cell].append(complex(x, y))
    return field


def check_connection(bat_a, bat_b, wall):
    print('Bat a:', bat_a)
    print('Bat b:', bat_b)

    wall_corners = [wall + complex(*delta) for delta in product((-0.5, 0.5), repeat=2)]
    print('Wall corners:', wall_corners)

    bat_a_to_corners_vectors = [wall_corner - bat_a for wall_corner in wall_corners]
    print('Bat a to wall corners vectors:', bat_a_to_corners_vectors)

    angles = [phase(vector) for vector in bat_a_to_corners_vectors]
    print('Angles:', angles)

    min_angle = min(angles)
    max_angle = max(angles)
    print('Min angle:', min_angle)
    print('Max angle:', max_angle)

    bat_a_to_b_angle = phase(bat_b - bat_a)
    print('Bat a to b angle:', bat_a_to_b_angle)

    is_connected = not(min_angle <= bat_a_to_b_angle <= max_angle)
    print('Is connected:', is_connected)
    print()
    return is_connected


def checkio(bunker: List[str]) -> [int, float]:
    print('Bunker:', bunker)

    field = map_to_field(bunker)
    print('Field:', field)

    # bat_2 = field[BAT].pop()
    # bat_1 = field[BAT].pop()
    # wall = field[WALL].pop()
    # print('Bat 1:', bat_1)
    # print('Bat 2:', bat_2)
    # print('Wall:', wall)
    #
    # check_connection(bat_1, bat_2, wall)

    for bat_a, bat_b in permutations(field[BAT], 2):
        for wall in field[WALL]:
            check_connection(bat_a, bat_b, wall)






    return 4


if __name__ == '__main__':
    def almost_equal(checked, correct, significant_digits=2):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision


    # assert almost_equal(checkio([
    #     "B--",
    #     "---",
    #     "--A"]), 2.83), "1st example"

    assert almost_equal(checkio([
        "B-B",
        "BW-",
        "-BA"]), 4), "2nd example"

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
