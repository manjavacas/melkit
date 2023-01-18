from melkit.gen_tools import *
import sys

def run(filename):

    # --------------- CVs --------------- #

    # Read CVs from file
    cvs = read_volumes(filename)

    # Find CV by ID
    cv001 = id_search(cvs, id='CV001')
    cv002 = id_search(cvs, id='CV002')

    # Edit CV attribute
    cv001.name = 'LLC'
    # print(cv001)

    cv002.name = 'Corridor'
    # print(cv002)

    # Change CV in file
    ## TO-DO ##

    # --------------- FLs --------------- #
    
    # Read FLs from file
    fls = read_flowpaths(filename)

    # Find FL by ID
    fl001 = id_search(fls, id='FL001')
    # print(fl001)


if __name__ == '__main__':
    run(sys.argv[1])