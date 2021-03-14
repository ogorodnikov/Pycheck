from functools import singledispatchmethod


class VoiceCommand:
    def __init__(self, channels):
        self.channels = channels
        self.current_channel_index = 0

    def set_channel(self, channel_index):
        self.current_channel_index = channel_index
        return self.channels[channel_index]

    def first_channel(self):
        return self.set_channel(0)

    def last_channel(self):
        return self.set_channel(-1)

    def turn_channel(self, channel_number):
        return self.set_channel(channel_number - 1)

    def next_channel(self):
        next_channel_index = (self.current_channel_index + 1) % len(self.channels)
        return self.set_channel(next_channel_index)

    def previous_channel(self):
        previous_channel_index = (self.current_channel_index - 1) % len(self.channels)
        return self.set_channel(previous_channel_index)

    def current_channel(self):
        return self.channels[self.current_channel_index]

    @singledispatchmethod
    def is_exist(self, *args, **kwargs):
        print('Basic is_exist')

    @is_exist.register(int)
    def _(self, channel):
        is_channel_found = 0 < channel <= len(self.channels)
        return ("No", "Yes")[is_channel_found]

    @is_exist.register(str)
    def _(self, channel):
        is_channel_found = channel in self.channels
        return ("No", "Yes")[is_channel_found]


if __name__ == '__main__':
    CHANNELS = ["BBC", "Discovery", "TV1000"]

    controller = VoiceCommand(CHANNELS)

    assert controller.first_channel() == "BBC"
    assert controller.last_channel() == "TV1000"
    assert controller.turn_channel(1) == "BBC"
    assert controller.next_channel() == "Discovery"
    assert controller.previous_channel() == "BBC"
    assert controller.current_channel() == "BBC"
    assert controller.is_exist(4) == "No"
    assert controller.is_exist("TV1000") == "Yes"