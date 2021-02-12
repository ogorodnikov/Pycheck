from datetime import datetime
from itertools import starmap
from typing import List


def get_seconds_between(start_time, end_time):
    return (end_time - start_time).total_seconds()


def sum_light(els: List[datetime]) -> int:
    print('Elements:', els)

    time_pairs = iter(els)
    turned_on_time = sum(starmap(get_seconds_between, zip(time_pairs, time_pairs)))

    print('Turned on time:', turned_on_time)
    print()
    return turned_on_time


if __name__ == '__main__':
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
    ]) == 610

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ]) == 1220

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
        datetime(2015, 1, 12, 11, 10, 10),
        datetime(2015, 1, 12, 12, 10, 10),
    ]) == 4820

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 1),
    ]) == 1

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 13, 11, 0, 0),
    ]) == 86410
