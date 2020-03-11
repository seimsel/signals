from numpy import linspace

class Scope:
    def __init__(self, address):
        self.id = id(self)
        self.address = address
        self.channels = []
        self.channel_types = []

    def add_channel(self, channel):
        channel.scope = self

        channel_number = sum(type(ch) == type(channel) for ch in self.channels)

        if channel_number:
            channel.name = f'{channel.name}{channel_number}'

        self.channels.append(channel)

    def get_channel_by_name(self, name):
        return next(filter(
            lambda channel: channel.name == name,
            self.channels))

    def get_channel_type_by_name(self, name):
        return next(filter(
            lambda channel_type: channel_type.__name__ == name,
            self.channel_types))
