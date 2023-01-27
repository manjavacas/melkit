from os import remove
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

    def remove_cv(self, cv_id, new_file=None):
        '''
        Deletes the records of a CV in an input file.
        '''

        new_file = new_file or self.filename + '_NEW'

        with open(self.filename, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if not line.startswith(cv_id):
                    f2.write(line)

    def write_cv(self, cv, new_file=None):
        '''
        Writes a new CV in an input file.
        '''

        new_file = new_file or self.filename + '_NEW'

        with open(self.filename, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith('CV') and not written:
                    f2.write(str(cv) + '\n' + line)
                    written = True
                else:
                    f2.write(line)

    def remove_comments(self, new_file=None):
        '''
        Remove comments from input file.
        '''

        new_file = new_file or self.filename + '_NEW'

        with open(self.filename, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if '*EOR*' in line or line.startswith('.') or not line.startswith('*'):
                    f2.write(line)
                elif '*' in line:
                    f2.write(line[:line.find('*')])

    def update_cv(self, cv, new_file=None):
        '''
        Updates CV input information.
        '''

        cv_id = list(cv.records.keys())[0][:5]

        tmp_file = self.filename + '_TMP'
        new_file = new_file or self.filename + '_NEW'

        self.remove_cv(cv_id, new_file=tmp_file)

        with open(tmp_file, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith('CV') and not written:
                    f2.write(str(cv) + '\n' + line)
                    written = True
                else:
                    f2.write(line)

        remove(self.filename + '_TMP')

    def id_search(self, list, id):
        '''
        Searches for an input object (CV, FL...) by its ID in a list of input elements.
        '''
        return [x for x in list if f'{id}00' in x.records.keys()][0]
