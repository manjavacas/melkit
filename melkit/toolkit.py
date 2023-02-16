'''
MELGEN/MELCOR file manipulation tools.
'''

from pandas import DataFrame, read_csv

from os import remove
from re import search, match

from typing import List, Union

from .exceptions import ParseException
from .inputs import Object, CV, FL
from .constants import CV_KEYS


class Toolkit:
    '''
    Multi-purpose file manipulator.
    '''

    def __init__(self, filename: str):
        self._filename = filename

        self._cv_list = self._read_cvs()
        self._fl_list = self._read_fls()

#------------------------ OBJECT MANIPULATION TOOLS -----------------------#

    def _read_object(self, id_regex: str) -> List[Object]:
        '''
        Looks for objects in the input file according to a given ID regex
        '''
        ids, objs = [], []
        with open(self._filename, 'r') as file:
            for line in file:
                id = search(id_regex, line)
                if id and id not in ids:
                    if 'CV' in id_regex:
                        objs.append(self.get_cv(id.group()[:-2]))
                    elif 'FL' in id_regex:
                        objs.append(self.get_fl(id.group()[:-2]))
        return objs

    def _read_cvs(self) -> List[CV]:
        '''
        Looks for CVs in the input file and returns them as a list of CV objects.
        '''
        return self._read_object(r'\bCV\d{3}00\b')

    def _read_fls(self) -> List[FL]:
        '''
        Looks for FLs in the input file and returns them as a list of FL objects.
        '''
        return self._read_object(r'\bFL\d{3}00\b')

    def get_cv(self, cv_id: str) -> CV:
        '''
        Searches for a CV in the input file and returns it as a CV object.
        '''
        cv_data = {}

        with open(self._filename, 'r') as file:
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

    def get_fl(self, fl_id: str) -> FL:
        '''
        Searches for a FL in the input file and returns it as a FL object.
        '''
        fl_data = {}

        with open(self._filename, 'r') as file:
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
                        elif match(r'.*T[0-9]', termination):
                            record_data['NTFLAG'] = record[1]
                            record_data['NFUN'] = record[2]
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

    def get_cv_list(self) -> List[CV]:
        '''
        Return the list of CVs in parsed file.
        '''
        return self._cv_list

    def get_fl_list(self) -> List[FL]:
        '''
        Return the list of CVs in parsed file.
        '''
        return self._fl_list

    def remove_object(self, obj_id: str, src_file: str = None, new_file: str = None) -> None:
        '''
        Deletes an object from the input file.
        '''

        src_file = src_file or self._filename
        new_file = new_file or self._filename + '_NEW'

        with open(src_file, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if not line.startswith(obj_id):
                    f2.write(line)

    def remove_objects(self, obj_ids: List[str], src_file: str = None, new_file: str = None) -> None:
        '''
        Deletes a list of objects from the input file.
        '''

        src_file = src_file or self._filename
        new_file = new_file or self._filename + '_NEW'

        with open(src_file, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if line[:5] not in obj_ids:
                    f2.write(line)

    def write_object(self, obj: Object, src_file: str = None, new_file: str = None) -> None:
        '''
        Writes a new object in the input file.
        '''

        src_file = src_file or self._filename
        new_file = new_file or self._filename + '_NEW'

        with open(src_file, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith('.') and not written:
                    f2.write('*\n' + str(obj) + '*\n' + line)
                    written = True
                else:
                    f2.write(line)

    def write_objects(self, obj_list: List[Object], src_file: str = None, new_file: str = None) -> None:
        '''
        Writes a new object in the input file.
        '''

        src_file = src_file or self._filename
        new_file = new_file or self._filename + '_NEW'

        with open(src_file, 'r') as f1, open(new_file, 'w') as f2:
            written = False
            for line in f1:
                if line.startswith('.') and not written:
                    for obj in obj_list:
                        f2.write('*\n' + str(obj) + '*\n')
                    f2.write(line)
                    written = True
                else:
                    f2.write(line)

    def update_object(self, obj: Object, src_file: str = None, new_file: str = None) -> None:
        '''
        Updates object input information.
        '''

        src_file = src_file or self._filename
        tmp_file = self._filename + '_TMP'
        new_file = new_file or self._filename + '_NEW'

        obj_id = obj.get_id()

        self.remove_object(obj_id, new_file=tmp_file)
        self.write_object(obj, src_file=tmp_file, new_file=new_file)

        remove(self._filename + '_TMP')

    def update_objects(self, obj_list: Object, src_file: str = None, new_file: str = None) -> None:
        '''
        Updates objects input information.
        '''

        src_file = src_file or self._filename
        tmp_file = self._filename + '_TMP'
        new_file = new_file or self._filename + '_NEW'

        obj_ids = [obj.get_id() for obj in obj_list]

        self.remove_objects(obj_ids, new_file=tmp_file)
        self.write_objects(obj_list, src_file=tmp_file, new_file=new_file)

        remove(self._filename + '_TMP')

    def clear_objects(self, src_file: str = None, new_file: str = None) -> None:
        '''
        Removes every CV or FL in the input file.
        '''

        src_file = src_file or self._filename
        new_file = new_file or self._filename + '_NEW'

        with open(src_file, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if line[:2] not in ['CV', 'FL', 'CF', 'TF']:
                    f2.write(line)

#-------------------------------- EDF TOOLS -------------------------------#

    def get_edf_vars(self) -> List[str]:
        '''
        Returns a list of variable names based on EDF records in file.
        '''
        keys = ['TIME']
        with open(self._filename, 'r') as file:
            for line in file:
                if match(r'\bEDF\d{3}[A-Z][A-Z0-9]', line):
                    keys.append(line.split()[1])
        return keys

    def get_last_values(self, datafile: str) -> List[float]:
        '''
        Returns the last values of an EDF output file.
        '''
        with open(datafile, 'r') as file:
            for line in file:
                pass
            last_line = line
        return last_line.split()

    def get_last_values_dict(self, datafile: str) -> List[float]:
        '''
        Returns the last values of an EDF output file with the corresponding variable names.
        '''
        values = self.get_last_values(datafile)
        keys = ['TIME'] + self.get_edf_vars(datafile)

        return dict(zip(keys, values))

    def as_dataframe(self, datafile: str) -> DataFrame:
        '''
        Converts an output EDF file to a Pandas dataframe.
        '''
        df = read_csv(datafile, sep='\s+', header=None)
        df.columns = self.get_edf_vars()
        return df

    def plot_edf(self, datafile: str, y_var: str) -> None:
        '''
        Plot an EDF variable value along time.
        '''
        import matplotlib.pyplot as plt
        self.as_dataframe(datafile).plot(x='TIME', y=y_var)
        plt.show()

#----------------------------- CONNECTION TOOLS ---------------------------#

    def get_fl_connections(self, cv_id: str) -> List[FL]:
        '''
        Get those FLs connected to a given CV
        '''
        fl_connected = []
        for fl in self._fl_list:
            if cv_id[2:] in [fl.get_field('KCVFM'), fl.get_field('KCVTO')]:
                fl_connected.append(fl)
        return fl_connected

    def get_connected_cvs(self, cv_id: str) -> List[CV]:
        '''
        Get those CVs connected to a given CV
        '''
        fl_connected = self.get_fl_connections(cv_id)
        cv_connected = []
        for fl in fl_connected:
            if cv_id[2:] == fl.get_field('KCVFM'):
                cv_connected.append(self.id_search(
                    self._cv_list, 'CV' + fl.get_field('KCVTO')))
            elif cv_id[2:] == fl.get_field('KCVTO'):
                cv_connected.append(self.id_search(
                    self._cv_list, 'CV' + fl.get_field('KCVFM')))
        return cv_connected

    def create_submodel(self, cv_id: str, new_file: str = None) -> Union[List[CV], List[FL]]:
        '''
        Creates a submodel related to a given CV. Those neighbour CVs are made time-independent.
        '''

        new_file = new_file or self._filename + '_SUB'
        tmp_file = self._filename + '_TMP'

        sub_cvs = self.get_connected_cvs(cv_id) + [self.get_cv(cv_id)]
        sub_fls = self.get_fl_connections(cv_id)

        # Make TIME-INDEPENDENT
        for cv in sub_cvs:
            cv.update_field('ICVACT', -1)

        # Create submodel file
        self.clear_objects(new_file=tmp_file)
        self.write_objects(sub_cvs + sub_fls,
                           src_file=tmp_file, new_file=new_file)

        remove(self._filename + '_TMP')

        return sub_cvs, sub_fls

#------------------------------- AUX TOOLS --------------------------------#

    def get_used_ids(self, obj_list: List[Object]) -> List[str]:
        '''
        Returns a sorted list of used IDs from a list of objects.
        '''
        used_ids = []
        for obj in obj_list:
            first_record = list(obj.records.keys())[0]
            if first_record.endswith('00'):
                used_ids.append(first_record[:5])
        used_ids.sort()
        return used_ids

    def get_available_ids(self, obj_list: List[Object]) -> List[str]:
        '''
        Returns a sorted list of available IDs from a list of objects.
        '''
        used_ids = self.get_used_ids(obj_list)
        available_ids = []
        for i in range(1, 1000):
            id = f'{i:03}'
            if id not in used_ids:
                available_ids.append(id)
        return available_ids

    def remove_comments(self, new_file: str = None) -> None:
        '''
        Remove comments from input file.
        '''

        new_file = new_file or self._filename + '_NEW'

        with open(self._filename, 'r') as f1, open(new_file, 'w') as f2:
            for line in f1:
                if line.startswith('*') and '*EOR*' not in line:
                    f2.write('')
                elif '*' in line and '*EOR*' not in line:
                    f2.write(line[:line.find('*')] + '\n')
                else:
                    f2.write(line)

    def id_search(self, obj_list: List[Object], id: str) -> Object:
        '''
        Searches for an input object (CV, FL...) by its ID in a list of input elements.
        '''
        return [x for x in obj_list if f'{id}00' in x.records.keys()][0]

    def get_duplicated(self, obj_list: List[Object]) -> List[Object]:
        '''
        Searches for duplicated objects (CV, FL...) from a list of objects. 
        '''
        return list(set([x for x in obj_list if obj_list.count(x) > 1]))
