from melkit.toolkit import Toolkit
import sys

def run(filename):

    toolkit = Toolkit(filename)

    # --------------- CVs --------------- #

    # Read CVs from file
    cvs = toolkit.read_cvs()

    # Find CV by ID
    cv001 = toolkit.id_search(cvs, id='CV001')
    # cv002 = id_search(cvs, id='CV002')

    # Edit CV attribute
    cv001.name = 'LLC'
    print(cv001)

    # cv002.name = 'Corridor'
    # print(cv002)

    # Change CV in file
    toolkit.edit_cv(cv001)

    # --------------- FLs --------------- #
    
    # Read FLs from file
    # fls = read_flowpaths(filename)

    # Find FL by ID
    # fl001 = id_search(fls, id='FL001')
    # print(fl001)


if __name__ == '__main__':
    run(sys.argv[1])