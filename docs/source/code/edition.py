'''
Basic object editing from input file.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'
EDF_FILE = './edf_file.inp'


toolkit = Toolkit(INPUT_FILE)

toolkit.plot_edf(EDF_FILE)
