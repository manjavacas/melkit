from melkit.toolkit import Toolkit
from melkit.inputs import CV
import sys


def run(filename):

    toolkit = Toolkit(filename)

    # --------------- CVs --------------- #

    # Read CVs from file
    cvs = toolkit.read_cvs()

    # Find CV by ID
    cv001 = toolkit.id_search(cvs, id='CV001')

    # Edit CV attribute
    cv001.name = 'LLC'
    toolkit.update_cv(cv001, new_file='sample_files/test_edit.inp', ignore_comments=False)
    
    # Search CV by ID
    # cv001 = toolkit.id_search(cvs, id='CV001')

    # Write new CV
    # cv003 = CV(id='CV003')
    # toolkit.write_cv(cv003, new_file='sample_files/test_write.inp')

    # Remove CV
    # toolkit.remove_cv('CV003', new_file='sample_files/test_delete.inp')

    # --------------- FLs --------------- #

    # Read FLs from file
    # fls = read_flowpaths(filename)

    # Find FL by ID
    # fl001 = id_search(fls, id='FL001')
    # print(fl001)


if __name__ == '__main__':
    run(sys.argv[1])
