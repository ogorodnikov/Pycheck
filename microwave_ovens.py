from datetime import time


class MicrowaveTime(time):
    def __add__(self, other):
        seconds = self.second + other.second
        seconds = min(90 * 60, seconds)

        minutes, seconds = divmod(seconds, 60)
        minutes = minutes + self.minute + other.minute

        hours, minutes = divmod(minutes, 60)
        hours = hours + self.hour + other.hour

        return MicrowaveTime(hour=hours, minute=minutes, second=seconds)

    def __sub__(self, other):
        hour_sum = self.hour - other.hour
        minute_sum = self.minute - other.minute
        seconds_sum = self.second - other.second

        hour_sum = max(0, hour_sum)
        minute_sum = max(0, minute_sum)
        seconds_sum = max(0, seconds_sum)

        return MicrowaveTime(hour=hour_sum, minute=minute_sum, second=seconds_sum)


class MicrowaveBase:
    _time = None
    _faulty_segment = None

    def __init__(self):
        self.set_time('00:00')

    @staticmethod
    def string_to_time(time_string):

        hours = minutes = seconds = 0

        if time_string.find(':') > -1:
            minutes, seconds = map(int, time_string.split(':'))

        elif time_string.endswith('s'):
            time_value = int(time_string[:-1])
            minutes, seconds = divmod(time_value, 60)

        elif time_string.endswith('m'):
            time_value = int(time_string[:-1])
            minutes = time_value

        else:
            raise ValueError

        hours, minutes = divmod(minutes, 60)

        return MicrowaveTime(hour=hours, minute=minutes, second=seconds)

    def set_time(self, time_string):
        self._time = self.string_to_time(time_string)

    def add_time(self, time_string):
        self._time += self.string_to_time(time_string)

    def del_time(self, time_string):
        self._time -= self.string_to_time(time_string)

    def show_time(self):
        time_string = self._time.strftime('%M:%S')
        print('Time string:', time_string)

        faulty_time_string = ''.join('_' if i == self._faulty_segment
                                     else letter for i, letter in enumerate(time_string))

        print('Faulty time string:', faulty_time_string)
        return faulty_time_string


class Microwave1(MicrowaveBase):
    _faulty_segment = 0


class Microwave2(MicrowaveBase):
    _faulty_segment = 4


class Microwave3(MicrowaveBase):
    _faulty_segment = None


class RemoteControl:
    _microwave = None

    def __init__(self, microwave):
        self._microwave = microwave

    def set_time(self, time_string):
        self._microwave.set_time(time_string)

    def add_time(self, amount_of_time_string):
        self._microwave.add_time(amount_of_time_string)

    def del_time(self, amount_of_time_string):
        self._microwave.del_time(amount_of_time_string)

    def show_time(self):
        return self._microwave.show_time()


if __name__ == '__main__':
    microwave_1 = Microwave1()
    microwave_2 = Microwave2()
    microwave_3 = Microwave3()

    remote_control_1 = RemoteControl(microwave_1)
    remote_control_1.set_time("01:00")

    remote_control_2 = RemoteControl(microwave_2)
    remote_control_2.add_time("90s")

    remote_control_3 = RemoteControl(microwave_3)
    remote_control_3.del_time("300s")
    remote_control_3.add_time("100s")

    assert remote_control_1.show_time() == "_1:00"
    assert remote_control_2.show_time() == "01:3_"
    assert remote_control_3.show_time() == "01:40"

    # mision tests

    microwave_2 = Microwave2()
    rc_2 = RemoteControl(microwave_2)
    rc_2.set_time("89:00")
    rc_2.add_time("90s")
    rc_2.add_time("20m")
    rc_2.show_time()
