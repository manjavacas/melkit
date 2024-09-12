'''
Basic object editing from input file.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'
EDF_FILE = './edf_file.inp'


toolkit = Toolkit(INPUT_FILE)

cv = toolkit.get_cv('CV001')

# Edit CV field
cv.update_field('NAME', 'my_volume')

# Update in file
toolkit.update_object(cv)

# You can also edit several objects at the same time!
other_cv = toolkit.get_cv('CV002')
other_cv.update_field('ALTITUDE', 7.5)

toolkit.update_objects([cv, other_cv])