from datetime import time


class MicrowaveBase:
    _time = None

    def __init__(self):
        self.set_time('00:00')

    def set_time(self, time_string):
        minutes, seconds = map(int, time_string.split(':'))
        self._time = time(minute=minutes, second=seconds)

    def add_time(self, amount_of_time_string):
        if amount_of_time_string.endswith('s'):
            self._time += time.struct_time(tm_sec=amount_of_time_string[:-1])
            print('Self time:', self._time)
        elif amount_of_time_string.endswith('m'):
            pass
        else:
            raise ValueError


class Microwave1(MicrowaveBase):
    pass


class Microwave2(MicrowaveBase):
    pass


class Microwave3(MicrowaveBase):
    pass


class RemoteControl:
    _microwave = None

    def __init__(self, microwave):
        self._microwave = microwave

    def set_time(self, time_string):
        self._microwave.set_time(time_string)

    def add_time(self, amount_of_time_string):
        self._microwave.add_time(amount_of_time_string)


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
