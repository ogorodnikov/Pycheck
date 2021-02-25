from operator import itemgetter
from datetime import datetime, timedelta
from itertools import groupby, zip_longest
from typing import List, Optional, Union, Tuple


def sum_light(els: List[Union[datetime, Tuple[datetime, int]]],
              start_watching: Optional[datetime] = datetime.min,
              end_watching: Optional[datetime] = datetime.max,
              operating: Optional[timedelta] = timedelta.max,
              req: Optional[int] = 1) -> int:

    sorted_elements = sorted((1, element) if isinstance(element, datetime)
                             else tuple(reversed(element))
                             for element in els)

    grouped_elements = groupby(sorted_elements, key=itemgetter(0))

    intervals = []
    for button_index, pushes in grouped_elements:

        pushes = (push for _, push in pushes)
        duration_left = operating

        for start, end in zip_longest(pushes, pushes, fillvalue=datetime.max):

            duration = end - start
            limited_duration = min(duration, duration_left)
            duration_left -= limited_duration

            limited_interval = (start, start + limited_duration)
            intervals.append((limited_interval, button_index))

    watched_intervals = [((max(start, start_watching), min(end, end_watching)), button_index)
                         for (start, end), button_index in intervals
                         if end > start_watching and start < end_watching]

    if not watched_intervals:
        return 0

    events = [(button_index, event) for interval, button_index
              in watched_intervals for event in interval]

    sorted_events = sorted(events, key=itemgetter(1))

    lit_start = None
    lit_bulbs = set()
    lit_intervals = []

    for button_index, event_time in sorted_events:

        if button_index not in lit_bulbs:
            lit_bulbs |= {button_index}
        else:
            lit_bulbs -= {button_index}

        if len(lit_bulbs) >= req and not lit_start:
            lit_start = event_time

        if len(lit_bulbs) < req and lit_start:
            lit_intervals.append((lit_start, event_time))
            lit_start = None

    lit_time = sum((end - start).total_seconds() for start, end in lit_intervals)
    return lit_time


if __name__ == '__main__':

    is_old_asserts = True

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
            operating=timedelta(seconds=5)) == 10

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ], req=1) == 60

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ], req=2) == 10

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], req=1) == 40

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], req=2) == 20

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], req=3) == 0

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 50), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], req=3) == 10

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0), req=2) == 20

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0), req=2, operating=timedelta(seconds=15)) == 10

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
        (datetime(2015, 1, 12, 10, 1, 20), 2),
        (datetime(2015, 1, 12, 10, 1, 40), 2),
    ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=2) == 20

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
        (datetime(2015, 1, 12, 10, 1, 20), 2),
        (datetime(2015, 1, 12, 10, 1, 40), 2),
    ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=3) == 0

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 0), 4),
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
        (datetime(2015, 1, 12, 10, 1, 20), 2),
        (datetime(2015, 1, 12, 10, 1, 40), 2),
    ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100), req=3) == 20
