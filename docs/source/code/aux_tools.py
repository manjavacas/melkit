'''
Some auxiliary tools.
'''

from melkit.toolkit import Toolkit

INPUT_FILE = './input_file.inp'

toolkit = Toolkit(INPUT_FILE)

cv = toolkit.get_cv('CV001')
fls = toolkit.get_fl_list()

# Remove file comments
toolkit.remove_comments(new_file=INPUT_FILE + '_no_comments')

# Get duplicated objects in list    
toolkit.get_duplicated(fls)

# Get available IDs from object list
toolkit.get_available_ids(fls)

# Get connections for a given CV
toolkit.get_fl_connections(cv)
toolkit.get_connected_cvs(cv)



