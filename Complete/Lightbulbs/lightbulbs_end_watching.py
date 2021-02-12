from datetime import datetime
from typing import List, Optional


def sum_light(els: List[datetime], start_watching: Optional[datetime] = None,
              end_watching: Optional[datetime] = None) -> int:

    print('Elements:')
    for element in els:
        print(element)
    if len(els) % 2:
        els.append(datetime.max)
        print('Added maximum datetime at the end:')
        for element in els:
            print(element)

    print('Start watching:', start_watching)
    print('End watching:', end_watching)

    turned_on_time = 0
    time_pairs = iter(els)
    for start_time, end_time in zip(time_pairs, time_pairs):
        print('    Start time:', start_time)
        print('    End time:  ', end_time)
        if start_watching:
            if start_time < end_time <= start_watching:
                continue
            if start_time < start_watching < end_time:
                start_time = start_watching
        if end_watching:
            if end_watching <= start_time < end_time:
                continue
            if start_time < end_watching < end_time:
                end_time = end_watching

        turned_on_time += (end_time - start_time).total_seconds()
        print('    Turned on time:', turned_on_time)

    print('Turned on time:', turned_on_time)
    print()
    return turned_on_time


if __name__ == '__main__':
    print("Example:")
    print(sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10)))

    assert sum_light(els=[
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
        start_watching=datetime(2015, 1, 12, 10, 0, 0),
        end_watching=datetime(2015, 1, 12, 10, 0, 10)) == 10

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 7)) == 7

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
        datetime(2015, 1, 12, 10, 0, 3),
        datetime(2015, 1, 12, 10, 0, 10)) == 7

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
        datetime(2015, 1, 12, 10, 0, 10),
        datetime(2015, 1, 12, 10, 0, 20)) == 0

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 10, 30, 0),
        datetime(2015, 1, 12, 11, 0, 0)) == 0

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 10, 10, 0),
        datetime(2015, 1, 12, 11, 0, 0)) == 10

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 10, 10, 0),
        datetime(2015, 1, 12, 11, 0, 10)) == 20

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 9, 50, 0),
        datetime(2015, 1, 12, 10, 0, 10)) == 10

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 9, 0, 0),
        datetime(2015, 1, 12, 10, 5, 0)) == 300

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
        datetime(2015, 1, 12, 11, 5, 0),
        datetime(2015, 1, 12, 12, 0, 0)) == 310

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
        datetime(2015, 1, 12, 11, 5, 0),
        datetime(2015, 1, 12, 11, 10, 0)) == 300

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
        datetime(2015, 1, 12, 10, 10, 0),
        datetime(2015, 1, 12, 11, 0, 10)) == 20

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
        datetime(2015, 1, 12, 9, 10, 0),
        datetime(2015, 1, 12, 10, 20, 20)) == 610

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
        datetime(2015, 1, 12, 9, 10, 0),
        datetime(2015, 1, 12, 10, 20, 20)) == 1220

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
        datetime(2015, 1, 12, 9, 9, 0),
        datetime(2015, 1, 12, 10, 0, 0)) == 0

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
        datetime(2015, 1, 12, 9, 9, 0),
        datetime(2015, 1, 12, 10, 0, 10)) == 10

    print("The third mission in series is completed? Click 'Check' to earn cool rewards!")