'''
Basic object reading from input file.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'

toolkit = Toolkit(INPUT_FILE)

print('===== CONTROL VOLUMES =====')
for cv in toolkit.get_cv_list():
    print(cv)

print('===== FLOW PATHS =====')
for fl in toolkit.get_fl_list():
    print(fl)
