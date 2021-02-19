from collections import defaultdict
from typing import List

BAT = 'B'
ALPHA_BAT = 'A'
WALL = 'W'
EMPTY = '-'


def map_to_field(bunker_map):
    field = defaultdict(set)
    for y, row in enumerate(bunker_map):
        for x, cell in enumerate(row):
            field[cell] |= {complex(x, y)}
    return field


def checkio(bunker: List[str]) -> [int, float]:
    print('Bunker:', bunker)

    field = map_to_field(bunker)
    print('Field:', field)

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
