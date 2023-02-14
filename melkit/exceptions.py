'''
Custom MELKIT exceptions.
'''

class ParseException(Exception):
    '''
    Input parse exception.
    '''
    def __init__(self, obj, message='parse exception'):
        self.obj = obj
        self.message = '\n\t' + message
        super().__init__(f'[{obj}] {self.message}')
