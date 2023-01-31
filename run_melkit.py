from melkit.toolkit import Toolkit
from melkit.inputs import CV, FL
import sys

OUTPUT_FILE = 'OUTPUTS/VARIABLES.DAT'

def run(filename):

    toolkit = Toolkit(filename)

    print(toolkit.as_dataframe(OUTPUT_FILE))

if __name__ == '__main__':
    run(sys.argv[1])
