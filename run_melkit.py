from melkit.toolkit import Toolkit
from melkit.inputs import CV
import sys


def run(filename):

    toolkit = Toolkit(filename)

    # --------------- CVs --------------- #

    # cv001 = CV({
    #     'CV00100': {'CVNAME': 'R001', 'ICVTHR': 2, 'ICVFF': 0, 'ICVTYP': 1},
    #     'CV00101': {'IPFSW': 0, 'ICVACT': 0},
    #     'CV001A0': {'ITYPTH': 3},
    #     'CV001A1': {'PVOL': 101235},
    #     'CV001A2': {'TATM': 290.95, 'RHUM': 0.0},
    #     'CV001A3': {'MLFR.8': 0.9999},
    #     'CV001A3': {'MLFR.5': 0.000021},
    #     'CV001A3': {'MLFR.4': 0.000079},
    #     'CV001B1': {'ALTITUDE': 0.0, 'VOLUME': 0.0},
    #     'CV001B2': {'ALTITUDE': 7.2, 'VOLUME': 2658.7}
    # })
    # print(cv001)

    for cv in toolkit.read_cvs():
        print(cv)

    # print(toolkit.get_cv('CV001'))

if __name__ == '__main__':
    run(sys.argv[1])
