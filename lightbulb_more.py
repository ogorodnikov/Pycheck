from operator import itemgetter
from datetime import datetime, timedelta
from itertools import groupby, zip_longest
from typing import List, Optional, Union, Tuple


def sum_light(els: List[Union[datetime, Tuple[datetime, int]]],
              start_watching: Optional[datetime] = datetime.min,
              end_watching: Optional[datetime] = datetime.max,
              operating: Optional[timedelta] = timedelta.max,
              req: Optional[int] = 1) -> int:
    sorted_elements = sorted((1, e) if isinstance(e, datetime) else tuple(reversed(e)) for e in els)

    grouped_elements = groupby(sorted_elements, key=itemgetter(0))

    intervals = []
    for button_index, button_pushes in grouped_elements:

        duration_left = operating
        pushes = [button_push for _, button_push in button_pushes]
        pushes_iter = iter(pushes)

        for interval in zip_longest(pushes_iter, pushes_iter, fillvalue=datetime.max):
            interval_start, interval_end = interval

            duration = interval_end - interval_start
            limited_duration = min(duration, duration_left)
            duration_left -= limited_duration

            limited_interval = (interval_start, interval_start + limited_duration)
            intervals.append((limited_interval, button_index))

    watched_intervals = [((max(start, start_watching), min(end, end_watching)), button_index)
                         for (start, end), button_index in intervals
                         if end > start_watching and start < end_watching]

    if not watched_intervals:
        return 0

    sorted_intervals = sorted(watched_intervals)

    print('Sorted elements:')
    [print(e) for e in sorted_elements]
    print()
    print('Intervals:')
    [print(e) for e in intervals]
    print()
    print('Watched intervals:')
    [print(e) for e in watched_intervals]
    print()

    lit_start = datetime.max
    lit_end = datetime.min
    lit_intervals = []
    for (start, end), button_index in sorted_intervals:
        if lit_start <= start <= lit_end:
            lit_end = max(lit_end, end)
        else:
            lit_intervals.append((lit_start, lit_end))
            lit_start = start
            lit_end = end
    lit_intervals = lit_intervals[1:] + [(lit_start, lit_end)]

    lit_time = sum((end - start).total_seconds() for start, end in lit_intervals)
    print('Lit time:', lit_time)
    print()
    print('============================')

    events = [(button_index, event) for interval, button_index in watched_intervals for event in interval]
    sorted_events = sorted(events, key=itemgetter(1))

    print('Events:')
    [print(e) for e in events]
    print()
    print('Sorted events:')
    [print(e) for e in sorted_events]
    print()

    req_start = None
    req_intervals = []

    lit_bulbs = set()
    for button_index, event in sorted_events:
        print()
        print('Button index:', button_index)
        print('Event:', event)

        if button_index not in lit_bulbs:
            lit_bulbs |= {button_index}
        else:
            lit_bulbs -= {button_index}

        print('Lit bulbs:', lit_bulbs)

        if len(lit_bulbs) >= req and req_start == None:
            print('Starting')
            req_start = event
        if len(lit_bulbs) < req and req_start != None:
            print('Ending')
            req_intervals.append((req_start, event))
            req_start = None

    print('Req intervals:')
    [print(e) for e in req_intervals]
    print()

    req_time = sum((end - start).total_seconds() for start, end in req_intervals)
    print('Req time:', req_time)

    return req_time


if __name__ == '__main__':

    is_old_asserts = False

    if is_old_asserts:
        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ]) == 60

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 11, 0, 0), 2),
            (datetime(2015, 1, 12, 11, 1, 0), 2),
        ]) == 70

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ]) == 30

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ]) == 40

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
            (datetime(2015, 1, 12, 10, 1, 0), 3),
            (datetime(2015, 1, 12, 10, 1, 20), 3),
        ]) == 60

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], datetime(2015, 1, 12, 10, 0, 50)) == 10

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 30)) == 20

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 20)) == 30

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 10)) == 30

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 50)) == 0

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 30)) == 20

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 20)) == 30

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
            (datetime(2015, 1, 12, 10, 1, 20), 2),
            (datetime(2015, 1, 12, 10, 1, 40), 2),
        ], datetime(2015, 1, 12, 10, 0, 20)) == 50

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], datetime(2015, 1, 12, 10, 0, 30), datetime(2015, 1, 12, 10, 1, 0)) == 30

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], datetime(2015, 1, 12, 10, 0, 20), datetime(2015, 1, 12, 10, 1, 0)) == 40

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            datetime(2015, 1, 12, 10, 0, 10),
        ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 0, 30)) == 30

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0)) == 40

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 0, 10)) == 0

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
        ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 20)) == 10

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
        ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 20)) == 10

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
        ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 30)) == 20

        assert sum_light(els=[
            (datetime(2015, 1, 11, 0, 0, 0), 3),
            datetime(2015, 1, 12, 0, 0, 0),
            (datetime(2015, 1, 13, 0, 0, 0), 3),
            (datetime(2015, 1, 13, 0, 0, 0), 2),
            datetime(2015, 1, 14, 0, 0, 0),
            (datetime(2015, 1, 15, 0, 0, 0), 2),
        ], start_watching=datetime(2015, 1, 10, 0, 0, 0), end_watching=datetime(2015, 1, 16, 0, 0, 0)) == 345600

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 10),
        ], operating=timedelta(seconds=100)) == 10

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 10),
        ], operating=timedelta(seconds=5)) == 5

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 10),
            (datetime(2015, 1, 12, 10, 0, 0), 2),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], operating=timedelta(seconds=100)) == 60

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 30),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], operating=timedelta(seconds=100)) == 60

        assert sum_light([
            datetime(2015, 1, 12, 10, 0, 0),
            datetime(2015, 1, 12, 10, 0, 30),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            (datetime(2015, 1, 12, 10, 1, 0), 2),
        ], operating=timedelta(seconds=20)) == 40

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
            (datetime(2015, 1, 12, 10, 1, 0), 3),
            (datetime(2015, 1, 12, 10, 1, 20), 3),
        ], operating=timedelta(seconds=10)) == 30

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
            (datetime(2015, 1, 12, 10, 1, 20), 2),
            (datetime(2015, 1, 12, 10, 1, 40), 2),
        ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100)) == 50

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
            datetime(2015, 1, 12, 10, 0, 40),
            (datetime(2015, 1, 12, 10, 0, 50), 2),
            (datetime(2015, 1, 12, 10, 1, 20), 2),
            (datetime(2015, 1, 12, 10, 1, 40), 2),
        ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=10)) == 20

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
        ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
            operating=timedelta(seconds=20)) == 20

        assert sum_light([
            (datetime(2015, 1, 12, 10, 0, 10), 3),
            datetime(2015, 1, 12, 10, 0, 20),
            (datetime(2015, 1, 12, 10, 0, 30), 3),
            (datetime(2015, 1, 12, 10, 0, 30), 2),
        ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
            operating=timedelta(seconds=10)) == 20

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
    ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
        operating=timedelta(seconds=5)) == 100

    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     (datetime(2015, 1, 12, 10, 0, 0), 2),
    #     datetime(2015, 1, 12, 10, 0, 10),
    #     (datetime(2015, 1, 12, 10, 1, 0), 2),
    # ], req=1) == 60
    #
    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     (datetime(2015, 1, 12, 10, 0, 0), 2),
    #     datetime(2015, 1, 12, 10, 0, 10),
    #     (datetime(2015, 1, 12, 10, 1, 0), 2),
    # ], req=2) == 10

    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], req=1) == 40
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], req=2) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], req=3) == 0
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 50), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], req=3) == 10
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0), req=2) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    # ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0), req=2, operating=timedelta(seconds=15)) == 10
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    #     (datetime(2015, 1, 12, 10, 1, 20), 2),
    #     (datetime(2015, 1, 12, 10, 1, 40), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=2) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    #     (datetime(2015, 1, 12, 10, 1, 20), 2),
    #     (datetime(2015, 1, 12, 10, 1, 40), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=3) == 0
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 0), 4),
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    #     (datetime(2015, 1, 12, 10, 1, 20), 2),
    #     (datetime(2015, 1, 12, 10, 1, 40), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=3) == 20
