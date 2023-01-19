import re

from .inputs import CV, FL


class Toolkit:

    def __init__(self, filename):
        self.filename = filename

    def read_cvs(self):
        with open(self.filename, 'r') as file:
            lines = file.read().split('\n')

        cv_ids = set(re.findall(r'CV\d{3}(?!00)', '\n'.join(lines)))

        cvs = []
        for id in cv_ids:
            cv = CV(id=id)
            for line in lines:
                record = line.split()
                if record[0] == id + '00':
                    cv.name = record[1]
                elif record[0] == id + 'B2':
                    cv.height, cv.volume = record[1:3]
                elif record[0][0:6] == id + 'A':
                    if 'PVOL' in record:
                        cv.pressure = record[record.index('PVOL') + 1]
                    if 'TATM' in record:
                        cv.temperature = record[record.index('TATM') + 1]
                    if 'RHUM' in record:
                        cv.humidity = record[record.index('RHUM') + 1]

                    if 'MLFR.3' in record:
                        cv.h2o = record[record.index('MLFR.3') + 1]
                    elif 'MLFR.4' in record:
                        cv.n2 = record[record.index('MLFR.4') + 1]
                    elif 'MLFR.5' in record:
                        cv.o2 = record[record.index('MLFR.5') + 1]
                    elif 'MLFR.8' in record:
                        cv.ar = record[record.index('MLFR.8') + 1]

            cvs.append(cv)

        return cvs

    def read_flowpaths(self):
        with open(self.filename, 'r') as file:
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

    def edit_cv(self, id):
        pass

    def id_search(self, element_list, id):
        return [x for x in element_list if x.id == id][0]
