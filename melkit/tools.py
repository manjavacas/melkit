import re

from .elements import CV, FL

def extract_field(pattern, content):
    match = re.search(pattern, content)
    return content[match.end():].split()[0] if match else None


def read_volumes(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Get IDs
    cv_ids = set(re.findall(r'CV\d{3}', content))
    
    cvs = []
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


def get_cv(cvs, id):
    return [cv for cv in cvs if cv.id == id][0]

