from numpy import linspace

class Scope:
    def __init__(self, address):
        self.id = id(self)
        self.address = address
        self.channels = []
        self.channel_types = []

        self._t = None
        self._t_needs_refresh = True

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in ['sample_frequency', 'sample_depth']:
            self._t_needs_refresh = True

    @property
    def t(self):
        if self._t_needs_refresh:
            self._t = linspace(0,
                self.sample_depth/self.sample_frequency,
                self.sample_depth)
        
        return self._t

    def add_channel(self, channel):
        channel.scope = self
        self.channels.append(channel)

    def get_channel_by_name(self, name):
        return next(filter(
            lambda channel: channel.name == name,
            self.channels))

    def get_channel_type_by_name(self, name):
        return next(filter(
            lambda channel_type: channel_type.__name__ == name,
            self.channel_types))
