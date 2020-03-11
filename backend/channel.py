class Channel:
    def __init__(self, name):
        self.id = id(self)
        self.name = name

        self.parameters = []

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
