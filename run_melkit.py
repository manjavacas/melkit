from melkit.toolkit import Toolkit
from melkit.inputs import CV, FL
import sys

import matplotlib.pyplot as plt

OUTPUT_FILE = 'OUTPUTS/VARIABLES.DAT'

def run(filename):

    toolkit = Toolkit(filename)

    df = toolkit.as_dataframe(OUTPUT_FILE)
    print(df)
    df.plot(x='TIME', y='CVH-P.16')
    plt.show()

if __name__ == '__main__':
    run(sys.argv[1])
