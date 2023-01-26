
from re import search, match
from .exceptions import ParseException
from .inputs import CV
from .constants import CV_KEYS


class Toolkit:

    def __init__(self, filename):
        self.filename = filename

    def read_cvs(self):
        '''
        Looks for CVs in the input file and returns them as a list of CV objects.
        '''
        ids, cvs = [], []

        with open(self.filename, 'r') as file:
            for line in file:
                id = search(r'\bCV\d{3}00\b', line)
                if id and id not in ids:
                    cvs.append(self.get_cv(id.group()[:-2]))
        return cvs

    def get_cv(self, cv_id):
        '''
        Searches for a CV in the input file and returns it as a CV object.
        '''
        cv_data = {}

        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith(cv_id):
                    record = line.split()
                    record_id = record[0]
                    record_data = {}

                    try:
                        if record_id[-2:] == '00':
                            record_data['NAME'] = record[1]
                            record_data['ICVTHR'] = record[2]
                            record_data['ICVFF'] = record[3]
                            record_data['ICVTYP'] = record[4]
                        elif record_id[-2:] == '01':
                            record_data['IPFSW'] = record[1]
                            record_data['ICVACT'] = record[2]
                        elif record_id[-2:] == 'A0':
                            record_data['ITYPTH'] = record[1]
                        elif match(r'A[1-9]', record_id[-2:]):
                            for key in CV_KEYS:
                                if key in record:
                                    record_data[key] = record[record.index(
                                        key)+1]
                        elif match(r'B[1-9]', record_id[-2:]):
                            record_data['ALTITUDE'] = record[1]
                            record_data['VOLUME'] = record[2]
                        elif match(r'C[1-9]', record_id[-2:]):
                            record_data['CTYP'] = record[1]
                            record_data['IESTYP'] = record[2]
                            record_data['IESFLG'] = record[3]
                        else:
                            raise ParseException(
                                cv_id, f'Unknown record: {record_id}')
                    except:
                        raise ParseException(
                            cv_id, f'Invalid number of attributes for record {record_id}')
                    cv_data[record_id] = record_data

        return CV(cv_data)

    def update_cv(self):
        raise NotImplementedError

    def remove_cv(self, cv_id, new_file=None, ignore_comments=False):
        raise NotImplementedError

    def write_cv(self, cv, new_file=None, ignore_comments=False):
        raise NotImplementedError

    def id_search(self, element_list, id):
        raise NotImplementedError
