'''
Basic object reading from input file.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'

toolkit = Toolkit(INPUT_FILE)

# Read and show CVs file
for cv in toolkit.get_cv_list():
    print(cv)

# Read and show FLs in file
for fl in toolkit.get_fl_list():
    print(fl)