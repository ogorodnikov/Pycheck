from collections import Counter
from datetime import timedelta, date


def date_range(year):
    delta = timedelta(days=1)
    current_day = date(year=year, month=1, day=1)
    while current_day.year == year:
        yield int(current_day.strftime('%u'))
        current_day += delta


def weekday_int_to_str(weekday_int):
    weekday_datetime = date(year=1, month=1, day=weekday_int)
    return weekday_datetime.strftime('%A')


def most_frequent_days(a):
    print('Year:', a)

    weekday_counter = Counter(date_range(a))
    print('Weekday counter:', weekday_counter)

    max_count = max(weekday_counter.values())
    most_frequent_weekdays = sorted(weekday for weekday, count in weekday_counter.items() if count == max_count)
    print('Most frequent weekdays:', most_frequent_weekdays)

    most_frequent_weekday_names = list(map(weekday_int_to_str, most_frequent_weekdays))
    print('Most frequent weekday names:', most_frequent_weekday_names)

    print()
    return most_frequent_weekday_names


if __name__ == '__main__':
    assert most_frequent_days(1084) == ['Tuesday', 'Wednesday']
    assert most_frequent_days(1167) == ['Sunday']
    assert most_frequent_days(1216) == ['Friday', 'Saturday']
    assert most_frequent_days(1492) == ['Friday', 'Saturday']
    assert most_frequent_days(1770) == ['Monday']
    assert most_frequent_days(1785) == ['Saturday']
    assert most_frequent_days(212) == ['Wednesday', 'Thursday']
    assert most_frequent_days(1) == ['Monday']
    assert most_frequent_days(2135) == ['Saturday']
    assert most_frequent_days(3043) == ['Sunday']
    assert most_frequent_days(2001) == ['Monday']
    assert most_frequent_days(3150) == ['Sunday']
    assert most_frequent_days(3230) == ['Tuesday']
    assert most_frequent_days(328) == ['Monday', 'Sunday']
    assert most_frequent_days(2016) == ['Friday', 'Saturday']
