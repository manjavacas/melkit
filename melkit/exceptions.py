class ParseException(Exception):
    def __init__(self, cv, message='parse exception'):
        self.cv = cv
        self.message = '\n\t' + message
        super().__init__(f'[{cv}] {self.message}')
