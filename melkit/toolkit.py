from os import remove
from re import search, match
from .exceptions import ParseException
from .inputs import CV, FL
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

    def read_fls(self):
        '''
        Looks for FLs in the input file and returns them as a list of FL objects.
        '''
        ids, fls = [], []

        with open(self.filename, 'r') as file:
            for line in file:
                id = search(r'\bFL\d{3}00\b', line)
                if id and id not in ids:
                    fls.append(self.get_fl(id.group()[:-2]))
        return fls

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

                    termination = record_id[-2:]

                    try:
                        if termination == '00':
                            record_data['NAME'] = record[1]
                            record_data['ICVTHR'] = record[2]
                            record_data['ICVFF'] = record[3]
                            record_data['ICVTYP'] = record[4]
                        elif termination == '01':
                            record_data['IPFSW'] = record[1]
                            record_data['ICVACT'] = record[2]
                        elif termination == 'A0':
                            record_data['ITYPTH'] = record[1]
                        elif match(r'A[1-9]', termination):
                            for key in CV_KEYS:
                                if key in record:
                                    record_data[key] = record[record.index(
                                        key)+1]
                        elif match(r'B[1-9]', termination):
                            record_data['ALTITUDE'] = record[1]
                            record_data['VOLUME'] = record[2]
                        elif match(r'C[1-9]', termination):
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

    def get_fl(self, fl_id):
        '''
        Searches for a FL in the input file and returns it as a FL object.
        '''
        fl_data = {}

        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith(fl_id):
                    record = line.split()
                    record_id = record[0]
                    record_data = {}

                    termination = record_id[-2:]
                    # [!] Note that some terminations and fields have been ignored
                    try:
                        if termination == '00':
                            record_data['FLNAME'] = record[1]
                            record_data['KCVFM'] = record[2]
                            record_data['KCVTO'] = record[3]
                            record_data['ZFM'] = record[4]
                            record_data['ZTO'] = record[5]
                        elif termination == '01':
                            record_data['FLARA'] = record[1]
                            record_data['FLLEN'] = record[2]
                            record_data['FLOPO'] = record[3]
                            # record_data['FLHGTF'] = record[4]
                            # record_data['FLHGTT'] = record[5]
                        elif termination == '02':
                            record_data['KFLGFL'] = record[1]
                            record_data['KACTFL'] = record[2]
                            record_data['IBUBF'] = record[3]
                            record_data['IBUBT'] = record[4]
                        elif termination == '03':
                            record_data['FRICFO'] = record[1]
                            record_data['FRICRO'] = record[2]
                            # record_data['CDCHKF'] = record[3]
                            # record_data['CDCHKR'] = record[4]
                        elif termination == '04':
                            record_data['VLFLAO'] = record[1]
                            record_data['VLFLPO'] = record[2]
                        elif termination == '05':
                            record_data['XL2PF'] = record[1]
                        elif termination == '06':
                            record_data['IP2EDF'] = record[1]
                        elif termination == '0F':
                            record_data['ZBJFM'] = record[1]
                            record_data['ZTJFM'] = record[2]
                        elif termination == '0T':
                            record_data['ZBJTO'] = record[1]
                            record_data['ZTJTO'] = record[2]
                        elif match(r'B[0-9]', termination):
                            record_data['PKG'] = record[1]
                            record_data['OPTION'] = record[2]
                            record_data['ICORC1'] = record[3]
                            record_data['ICORC2'] = record[4]
                            record_data['FLMPTY'] = record[5]
                        elif match(r'S[0-9]', termination):
                            record_data['SAREA'] = record[1]
                            record_data['SLEN'] = record[2]
                            record_data['SHYD'] = record[3]
                            # record_data['SRGH'] = record[4]
                            # record_data['SLAM'] = record[5]
                            # record_data['ISFLT'] = record[6]
                        elif match(r'V[0-9]', termination):
                            record_data['NVTRIP'] = record[1]
                            record_data['NVFONF'] = record[2]
                            record_data['NVFONR'] = record[3]
                        else:
                            raise ParseException(
                                fl_id, f'Unknown record: {record_id}')
                    except:
                        raise ParseException(
                            fl_id, f'Invalid number of attributes for record {record_id}')
                    fl_data[record_id] = record_data

        return FL(fl_data)

    def remove_object(self, obj_id, new_file=None):
        '''
        Deletes an object from the input file.
        '''

        new_file = new_file or self.filename + '_NEW'

        with open(self.filename, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if not line.startswith(obj_id):
                    f2.write(line)

    def write_object(self, obj, new_file=None):
        '''
        Writes a new object in the input file.
        '''

        new_file = new_file or self.filename + '_NEW'

        obj_type = list(obj.records.keys())[0][:2]

        with open(self.filename, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith(obj_type) and not written:
                    f2.write(str(obj) + '\n' + line)
                    written = True
                else:
                    f2.write(line)

    def update_object(self, obj, new_file=None):
        '''
        Updates objects input information.
        '''

        obj_id = list(obj.records.keys())[0][:5]

        tmp_file = self.filename + '_TMP'
        new_file = new_file or self.filename + '_NEW'

        self.remove_object(obj_id, new_file=tmp_file)

        with open(tmp_file, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith('.') and not written:
                    f2.write(str(obj) + '*\n' + line)
                    written = True
                else:
                    f2.write(line)

        remove(self.filename + '_TMP')

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

    def id_search(self, obj_list, id):
        '''
        Searches for an input object (CV, FL...) by its ID in a list of input elements.
        '''
        return [x for x in obj_list if f'{id}00' in x.records.keys()][0]
