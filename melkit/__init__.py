'''
MELGEN/MELCOR file manipulation toolkit.
'''

import os

# Set version
version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
with open(version_file, 'r') as f:
    __version__ = f.read().strip()
