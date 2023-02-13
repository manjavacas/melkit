from .constants import CV_KEYS


class Object():
    def __init__(
        self,
        records=None
    ):
        self.records = records or {}

    def get_id(self):
        for record in self.records:
            if record.endswith('00'):
                return record[:5]

    def get_field(self, field_name):
        for record in self.records:
            if field_name in self.records[record]:
                return self.records[record][field_name]

    def update_field(self, field_name, new_val):
        for record in self.records:
            if field_name in self.records[record]:
                self.records[record][field_name] = new_val

    def __eq__(self, other):
        return self.get_id() == other.get_id()


class CV(Object):
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
    def __str__(self):
        fl_str = []
        for record, fields in self.records.items():
            fl_str.append(f'{record}\t')
            for value in fields.values():
                fl_str.append(f'{value}\t')
            fl_str.append('\n')
        return ''.join(fl_str)
