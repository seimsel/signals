class Channel:
    def __init__(self, name):
        self.id = id(self)
        self.name = name

        self.parameters = []

    def was_added(self):
        pass

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in ['scope']:
            self.was_added()

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
