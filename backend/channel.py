from numpy import linspace

class Channel:
    def __init__(self):
        self.id = id(self)
        self.name = type(self).__name__
        self.parameters = []

        self._t_needs_refresh = True

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in ['start_time', 'end_time', 'sample_depth']:
            self._t_needs_refresh = True

    @property
    def t(self):
        if self._t_needs_refresh:
            self._t = linspace(
                    self.start_time,
                    self.end_time,
                    self.sample_depth)
            self._t_needs_refresh = False

        return self._t

    @property
    def data(self):
        try:
            y = self.y # y needs to be accessed first, because it may change t
            t = self.t
        except Exception as e:
            print(e)
            y = None
            t = None

        return t, y

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
