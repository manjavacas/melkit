'''
Basic EDF visualization from input file.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'
EDF_FILE = './edf_file.inp'


toolkit = Toolkit(INPUT_FILE)

# Plot EDF values
toolkit.plot_edf(EDF_FILE)

# Get EDF vars registered
toolkit.get_edf_vars()

# Show last EDF values registered
toolkit.get_last_values_dict()