import re

from .inputs import CV, FL

# TO-REMOVE
def extract_field(pattern, content):
    match = re.search(pattern, content)
    return content[match.end():].split()[0] if match else None


def read_volumes(filename):
    with open(filename, 'r') as file:
        content = file.read()

    cv_ids = set(re.findall(r'CV\d{3}', content))

    cvs = []
    for id in cv_ids:
        cv = CV(id=id)
        
        # TO-IMPROVE
        cv.name = extract_field(id + '00\s+', content)
        cv.pressure = extract_field(id + '.*PVOL\s+', content)
        cv.humidity = extract_field(id + '.*RHUM\s+', content)
        cv.temperature = extract_field(id + '.*TATM\s+', content)
        cv.ar = extract_field(id + '.*MLFR.8\s+', content)
        cv.h2o = extract_field(id + '.*MLFR.3\s+', content)
        cv.n2 = extract_field(id + '.*MLFR.4\s+', content)
        cv.o2 = extract_field(id + '.*MLFR.5\s+', content)
        cv.height = extract_field(id + '.*B2\s+', content)
        cv.volume = extract_field(id + 'B2\s+\d*\.\d*\s+', content)

        cvs.append(cv)

    return cvs


def read_flowpaths(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n')

    fl_ids = set(re.findall(r'FL\d{3}(?!00)', '\n'.join(lines)))

    fls = []
    for id in fl_ids:
        fl = FL(id=id)
        for line in lines:
            record = line.split()
            if record[0] == id + '00':
                fl.name, fl.from_cv, fl.to_cv = record[1:4]
                if len(record) > 4:
                    fl.from_height, fl.to_height = record[4:6]
            elif record[0] == id + '01':
                fl.area, fl.length, fl.fraction_open = record[1:4]
            elif record[0] == id + '03':
                fl.forward_loss, fl.reverse_loss = record[1:3]
            elif record[0] == id + 'S0':
                fl.hyd_diam = record[3][:10]
        fls.append(fl)

    return fls


def id_search(element_list, id):
    return [x for x in element_list if x.id == id][0]


