from melkit.toolkit import Toolkit
from melkit.inputs import CV, FL
import sys


def run(filename):

    toolkit = Toolkit(filename)

    for cv in toolkit.read_cvs():
        print(cv)

    for fl in toolkit.read_fls():
        print(fl)
    
if __name__ == '__main__':
    run(sys.argv[1])
