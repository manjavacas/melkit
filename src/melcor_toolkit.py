import re
import sys

CARD_WIDTH = 22


class CV():
    def __init__(
        self,
        id,
        name=None,
        pressure=None,
        humidity=None,
        temperature=None,
        ar=None,
        h2o=None,
        n2=None,
        o2=None,
        altitude=None,
        volume=None
    ):
        self.id = id
        self.name = name
        self.pressure = pressure
        self.humidity = humidity
        self.temperature = temperature
        self.ar = ar
        self.h2o = h2o
        self.n2 = n2
        self.o2 = o2
        self.altitude = altitude
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
        from_altitude=None,
        to_altitude=None,
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
        self.from_altitude = from_altitude
        self.to_altitude = to_altitude
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


def extract_field(pattern, content):
    match = re.search(pattern, content)
    return content[match.end():].split()[0] if match else None


def read_CVs(filename):
    cvs = []

    with open(filename, 'r') as file:
        content = file.read()

    # Get IDs
    cv_ids = set(re.findall(r'CV\d{3}', content))

    for id in cv_ids:
        cv = CV(id=id)
        cv.name = extract_field(id + '00\s+', content)
        cv.pressure = extract_field(id + '.*PVOL\s+', content)
        cv.humidity = extract_field(id + '.*RHUM\s+', content)
        cv.temperature = extract_field(id + '.*TATM\s+', content)
        cv.ar = extract_field(id + '.*MLFR.8\s+', content)
        cv.h2o = extract_field(id + '.*MLFR.3\s+', content)
        cv.n2 = extract_field(id + '.*MLFR.4\s+', content)
        cv.o2 = extract_field(id + '.*MLFR.5\s+', content)
        cv.altitude = extract_field(id + '.*B2\s+', content)
        cv.volume = extract_field(id + 'B2\s+\d*\.\d*\s+', content)

        cvs.append(cv)

    return cvs


def get_CV(cvs, id):
    return [cv for cv in cvs if cv.id == id][0]


def run(filename):

    # --------------- CVs --------------- #

    # Read CVs from file
    cvs = read_CVs(filename)

    # Find CV by ID
    cv001 = get_CV(cvs, id='CV001')
    cv002 = get_CV(cvs, id='CV002')

    # Edit CV attribute
    cv001.name = 'LLC'
    print(cv001)

    cv002.name = 'Corridor'
    print(cv002)

    # Change CV in file
    ## TO-DO ##

    # --------------- FLs --------------- #
    ## TO-DO ##


if __name__ == '__main__':
    run(sys.argv[1])
