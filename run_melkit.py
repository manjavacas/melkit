from melkit.tools import *
import sys

def run(filename):

    # --------------- CVs --------------- #

    # Read CVs from file
    cvs = read_volumes(filename)

    # Find CV by ID
    cv001 = get_cv(cvs, id='CV001')
    cv002 = get_cv(cvs, id='CV002')

    # Edit CV attribute
    cv001.name = 'LLC'
    print(cv001)

    cv002.name = 'Corridor'
    print(cv002)

    # Change CV in file
    ## TO-DO ##

    # --------------- FLs --------------- #
    ## TO-DO ##

if __name__ == '__main__':
    run(sys.argv[1])