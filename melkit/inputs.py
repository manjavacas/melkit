from .constants import CV_KEYS


class Object():
    def __init__(
        self,
        records=None
    ):
        self.records = records or {}


class CV(Object):
    def __str__(self):
        cv_str = []
        for record_id, attributes in self.records.items():
            cv_str.append(f'{record_id}\t')
            for key, value in attributes.items():
                if key in CV_KEYS:
                    cv_str.append(f'{key}\t{value}\t')
                else:
                    cv_str.append(f'{value}\t')
            cv_str.append('\n')
        return ''.join(cv_str)


class FL(Object):

    def get_from(self):
        for key in list(self.records.keys()):
            if key.endswith('00'):
                return self.records[key]['KCVFM']

    def get_to(self):
        for key in list(self.records.keys()):
            if key.endswith('00'):
                return self.records[key]['KCVTO']

    def __str__(self):
        fl_str = []
        for record_id, attributes in self.records.items():
            fl_str.append(f'{record_id}\t')
            for value in attributes.values():
                fl_str.append(f'{value}\t')
            fl_str.append('\n')
        return ''.join(fl_str)
