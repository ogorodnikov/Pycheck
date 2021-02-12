from datetime import datetime


def text_to_seconds(text):
    seconds_per_unit = {'second': 1, 'minute': 60, 'hour': 3600}
    value, units = text.split()
    return sum(int(value) * seconds_per_unit[unit] for unit in seconds_per_unit if unit in units)


def broken_clock(starting_time, wrong_time, error_description):
    print('Starting time:', starting_time)
    print('Wrong time:', wrong_time)
    print('Error description:', error_description)

    shift, seconds = map(text_to_seconds, error_description.split(' at '))
    print('Shift:', shift)
    print('Seconds:', seconds)

    shift_per_seconds = shift / seconds
    print('Shift per seconds:', shift_per_seconds)

    start_datetime = datetime.strptime(starting_time, '%H:%M:%S')
    wrong_datetime = datetime.strptime(wrong_time, '%H:%M:%S')
    wrong_duration = wrong_datetime - start_datetime
    print('Wrong duration:', wrong_duration)

    real_duration = wrong_duration / (shift_per_seconds + 1)
    print('Real duration:', real_duration)

    real_datetime = start_datetime + real_duration
    real_time = real_datetime.strftime('%H:%M:%S')
    print('Real time:', real_time)
    print()
    return real_time


if __name__ == "__main__":
    assert broken_clock('00:00:00', '00:00:15', '+5 seconds at 10 seconds') == '00:00:10', "First example"
    assert broken_clock('06:10:00', '06:10:15', '-5 seconds at 10 seconds') == '06:10:30', 'Second example'
    assert broken_clock('13:00:00', '14:01:00', '+1 second at 1 minute') == '14:00:00', 'Third example'
    assert broken_clock('01:05:05', '04:05:05', '-1 hour at 2 hours') == '07:05:05', 'Fourth example'
    assert broken_clock('00:00:00', '00:00:30', '+2 seconds at 6 seconds') == '00:00:22', 'Fifth example'
