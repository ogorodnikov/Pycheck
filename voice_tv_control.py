class VoiceCommand:
    def __init__(self, channels):
        self.channels = channels
        self.current_channel = 0

    def set_channel(self, channel_index):
        self.current_channel = channel_index
        return self.channels[channel_index]

    def turn_channel(self, channel_number):
        return self.set_channel(channel_number - 1)

    def first_channel(self):
        return self.set_channel(0)

    def last_channel(self):
        return self.set_channel(-1)

    def next_channel(self):
        next_channel_index = (self.current_channel + 1) % len(self.channels)
        print('Next channel index:', next_channel_index)
        print('Self channels:', self.channels)
        return self.set_channel(next_channel_index)

if __name__ == '__main__':

    CHANNELS = ["BBC", "Discovery", "TV1000"]

    controller = VoiceCommand(CHANNELS)

    assert controller.first_channel() == "BBC"
    assert controller.last_channel() == "TV1000"
    assert controller.turn_channel(1) == "BBC"
    assert controller.next_channel() == "Discovery"
    # assert controller.previous_channel() == "BBC"
    # assert controller.current_channel() == "BBC"
    # assert controller.is_exist(4) == "No"
    # assert controller.is_exist("TV1000") == "Yes"
