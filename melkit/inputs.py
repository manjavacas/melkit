'''
MELGEN input objects.
'''

from .constants import CV_KEYS


class Object():
    '''
    Generic input object class.
    '''
    def __init__(
        self,
        records=None
    ):
        self.records = records or {}

    def get_id(self) -> str:
        for record in self.records:
            if record.endswith('00'):
                return record[:5]

    def get_field(self, field_name: str) -> str:
        for record in self.records:
            if field_name in self.records[record]:
                return self.records[record][field_name]

    def update_field(self, field_name: str, new_val: str) -> None:
        for record in self.records:
            if field_name in self.records[record]:
                self.records[record][field_name] = new_val

    def __eq__(self, other):
        return self.get_id() == other.get_id()
    
    def __str__(self):
        obj_str = []
        for record, fields in self.records.items():
            obj_str.append(f'{record}\t')
            for value in fields.values():
                obj_str.append(f'{value}\t')
            obj_str.append('\n')
        return ''.join(obj_str)


class CV(Object):
    '''
    Control Volume class (CVH package).
    '''
    def __str__(self):
        cv_str = []
        for record, fields in self.records.items():
            cv_str.append(f'{record}\t')
            for key, value in fields.items():
                if key in CV_KEYS:
                    cv_str.append(f'{key}\t{value}\t')
                else:
                    cv_str.append(f'{value}\t')
            cv_str.append('\n')
        return ''.join(cv_str)


class FL(Object):
    '''
    Flow Path class (FL package).
    '''

class CF(Object):
    '''
    Control Function class (CF package).
    '''
