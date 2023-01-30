from melkit.toolkit import Toolkit
from melkit.inputs import CV, FL
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

    # for cv in toolkit.read_cvs():
    #     print(cv)

    # print(toolkit.get_fl('CV001'))

    # cv_list = toolkit.read_objects()
    # print(toolkit.id_search(cv_list, 'CV001'))

    # toolkit.remove_object('CV001')
    # toolkit.remove_comments()

    # cv003 = CV({
    #     'CV00300': {'CVNAME': 'R003', 'ICVTHR': 2, 'ICVFF': 0, 'ICVTYP': 1},
    #     'CV00301': {'IPFSW': 0, 'ICVACT': 0},
    #     'CV003A0': {'ITYPTH': 3},
    #     'CV003A1': {'PVOL': 101235},
    #     'CV003A2': {'TATM': 290.95, 'RHUM': 0.0},
    #     'CV003A3': {'MLFR.8': 0.9999},
    #     'CV003A3': {'MLFR.5': 0.000021},
    #     'CV003A3': {'MLFR.4': 0.000079},
    #     'CV003B1': {'ALTITUDE': 0.0, 'VOLUME': 0.0},
    #     'CV003B2': {'ALTITUDE': 7.2, 'VOLUME': 2658.7}
    # })

    # toolkit.write_object(cv003)

    # cv001 = toolkit.get_cv('CV001')
    # cv001.records['CV00100']['CVNAME'] = 'FOO'
    # toolkit.update_object(cv001)

    # --------------- FLs --------------- #

    # for fl in toolkit.read_fls():
    #     print(fl)

    # fl002 = FL({
    #     'FL00200': {'FLNAME':'new-fl', 'KCVFM':'002', 'KCVTO':'001', 'ZFM':1.5, 'ZTO':1.6}
    # })

    # toolkit.write_object(fl002)

    # fl001 = toolkit.get_fl('FL001')
    # print(fl001)
    # fl001.records['FL00100']['FLNAME'] = 'FOO'
    # toolkit.update_object(fl001)

if __name__ == '__main__':
    run(sys.argv[1])
