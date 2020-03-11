class Parameter:
    def __init__(self, name, initialValue):
        self.id = id(self)
        self.name = name
        self.value = initialValue

class IntegerParameter(Parameter):
    pass

class FloatParameter(Parameter):
    pass

class SelectParameter(Parameter):
    def __init__(self, name, initialValue, options):
        super().__init__(name, initialValue)
        self.options = options

class SourceParameter(Parameter):
    def __init__(self, name, channel):
        super().__init__(name, None)
        self.channel = channel

    @property
    def options(self):
        if not self.channel.scope:
            return []

        return filter(
            lambda channelName: channelName != self.channel.name,
            map(
                lambda channel: channel.name,
                self.channel.scope.channels))
