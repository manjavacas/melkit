
from re import match

from .constants import CV_KEYS


class CV():
    def __init__(
        self,
        records=None
    ):
        self.records = records or {}

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


class FL():
    def __init__(
        self,
        records=None
    ):
        self.records = records or {}

    def __str__(self):
        cv_str = []
        for record_id, attributes in self.records.items():
            cv_str.append(f'{record_id}\t')
            for value in attributes.values():
                cv_str.append(f'{value}\t')
            cv_str.append('\n')
        return ''.join(cv_str)