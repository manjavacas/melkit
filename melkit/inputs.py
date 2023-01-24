from .constants import CARD_WIDTH


class CV():
    def __init__(
        self,
        id,
        name=None,
        pressure=0,
        humidity=0,
        temperature=0,
        ar=0,
        h2o=0,
        n2=0,
        o2=0,
        height=0,
        volume=0
    ):
        self.id = id
        self.name = self.id if not name else name
        self.pressure = pressure
        self.humidity = humidity
        self.temperature = temperature
        self.ar = ar
        self.h2o = h2o
        self.n2 = n2
        self.o2 = o2
        self.height = height
        self.volume = volume

    def __str__(self):
        cv_str = '╭-------- {} --------╮\n'.format(self.id)
        for attr, value in self.__dict__.items():
            l = len(str(attr) + ' = ' + str(value))
            cv_str += '| ' + f'{attr} = {value}' + \
                ' ' * (CARD_WIDTH - l) + '|\n'
        cv_str += '╰-----------------------╯\n'
        return cv_str


class FL():
    def __init__(
        self,
        id,
        name=None,
        from_cv=None,
        to_cv=None,
        from_height=None,
        to_height=None,
        area=None,
        length=None,
        hyd_diam=None,
        fraction_open=None,
        forward_loss=None,
        reverse_loss=None
    ):
        self.id = id
        self.name = name
        self.from_cv = from_cv
        self.to_cv = to_cv
        self.from_height = from_height
        self.to_height = to_height
        self.area = area
        self.length = length
        self.hyd_diam = hyd_diam
        self.fraction_open = fraction_open
        self.forward_loss = forward_loss
        self.reverse_loss = reverse_loss

    def __str__(self):
        fl_str = '╭-------- {} --------╮\n'.format(self.id)
        for attr, value in self.__dict__.items():
            l = len(str(attr) + ' = ' + str(value))
            fl_str += '| ' + f'{attr} = {value}' + \
                ' ' * (CARD_WIDTH - l) + '|\n'
        fl_str += '╰-----------------------╯\n'
        return fl_str
