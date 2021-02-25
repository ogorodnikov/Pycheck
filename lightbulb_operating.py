from datetime import datetime
from itertools import groupby, zip_longest
from operator import itemgetter
from typing import List, Optional, Union, Tuple


def print_iter(elements):
    for element in elements:
        print(element)


def sum_light(els: List[Union[datetime, Tuple[datetime, int]]],
              start_watching: Optional[datetime] = None,
              end_watching: Optional[datetime] = None) -> int:
    print('====================')
    print('Elements:')
    print_iter(els)
    print()

    sorted_elements = sorted((1, e) if isinstance(e, datetime) else tuple(reversed(e)) for e in els)
    print('Sorted:')
    print_iter(sorted_elements)
    print()

    grouped_elements = groupby(sorted_elements, key=itemgetter(0))

    intervals = []
    for button_index, button_pushes in grouped_elements:
        pushes = [button_push for _, button_push in button_pushes]
        pushes_iter = iter(pushes)
        for pair in zip_longest(pushes_iter, pushes_iter, fillvalue=datetime.max):
            intervals.append(pair)
    print('Intervals:')
    print_iter(intervals)
    print()

    if start_watching is None:
        start_watching = datetime.min
    if end_watching is None:
        end_watching = datetime.max
    print('Start watching:', start_watching)
    print('End watching:', end_watching)

    filtered_intervals = [(max(start, start_watching), min(end, end_watching))
                          for start, end in intervals
                          if end > start_watching and start < end_watching]
    print('Filtered intervals:')
    print_iter(filtered_intervals)
    print()

    if not filtered_intervals:
        print('Nothing filtered')
        return 0

    sorted_intervals = sorted(filtered_intervals)
    print('Sorted intervals:')
    print_iter(sorted_intervals)
    print()

    lit_start = datetime.max
    lit_end = datetime.min
    lit_intervals = []
    for start, end in sorted_intervals:
        print('Checking:', start, '-', end)
        if lit_start <= start <= lit_end:
            print('    Adjacent')
            lit_end = max(lit_end, end)
            print('    New lit end:   ', lit_start, '-', lit_end)
        else:
            print('    New interval:  ', start, '-', end)
            lit_intervals.append((lit_start, lit_end))
            print('    Writing closed:', lit_start, '-', lit_end)
            lit_start = start
            lit_end = end
        print('    Lit intervals: ', lit_intervals)
        print()
    lit_intervals = lit_intervals[1:] + [(lit_start, lit_end)]
    print('Lit intervals:')
    print_iter(lit_intervals)

    lit_time = sum((end - start).total_seconds() for start, end in lit_intervals)
    print('Lit time:', lit_time)
    print()
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

    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     datetime(2015, 1, 12, 10, 0, 10),
    # ], operating=timedelta(seconds=5)) == 5
    #
    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     datetime(2015, 1, 12, 10, 0, 10),
    #     (datetime(2015, 1, 12, 10, 0, 0), 2),
    #     (datetime(2015, 1, 12, 10, 1, 0), 2),
    # ], operating=timedelta(seconds=100)) == 60
    #
    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     datetime(2015, 1, 12, 10, 0, 30),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     (datetime(2015, 1, 12, 10, 1, 0), 2),
    # ], operating=timedelta(seconds=100)) == 60
    #
    # assert sum_light([
    #     datetime(2015, 1, 12, 10, 0, 0),
    #     datetime(2015, 1, 12, 10, 0, 30),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     (datetime(2015, 1, 12, 10, 1, 0), 2),
    # ], operating=timedelta(seconds=20)) == 40
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    #     datetime(2015, 1, 12, 10, 0, 40),
    #     (datetime(2015, 1, 12, 10, 0, 50), 2),
    #     (datetime(2015, 1, 12, 10, 1, 0), 3),
    #     (datetime(2015, 1, 12, 10, 1, 20), 3),
    # ], operating=timedelta(seconds=10)) == 30
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
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=100)) == 50
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
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 20), operating=timedelta(seconds=10)) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
    #     operating=timedelta(seconds=20)) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
    #     operating=timedelta(seconds=10)) == 20
    #
    # assert sum_light([
    #     (datetime(2015, 1, 12, 10, 0, 10), 3),
    #     datetime(2015, 1, 12, 10, 0, 20),
    #     (datetime(2015, 1, 12, 10, 0, 30), 3),
    #     (datetime(2015, 1, 12, 10, 0, 30), 2),
    # ], start_watching=datetime(2015, 1, 12, 10, 0, 10), end_watching=datetime(2015, 1, 12, 10, 0, 30),
    #     operating=timedelta(seconds=5)) == 10