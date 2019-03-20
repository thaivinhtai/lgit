"""This module simulates a very small concept of "git init" command, which will
create a "lgit repository" via make a specified directory.

Functions in this module:
    -   .....
    -   init(path)  ->  create a "lgit repository".
"""

from tools import *


def init(path=''):
    """
    init(path)  ->  create a "lgit repository".

    "lgit repository" is seen as a simulated repository of git. There is a
    folder named ".lgit", which has these following structure:
        -   a directory "objects" will store the files of "lgit add"
        -   a directory "commits" will store the commit objects: those are not
            the actual file listings but some information about the commit
            (author, date & commit message)
        -   a directory "snapshots" will store the actual file listings
        -   a file "index" will host the staging area & other information
        -   a file "config" will store the name of the author, initialised from
            the environment variable LOGNAME

    Optional argument:
        path    --  a string that specifies the path will store folder ".lgit",
                    default is current directory.
    """
    folders = ['.lgit', '.lgit/object', '.lgit/commits', '.lgit/snapshots']
    [mkdir(path + folder) for folder in folders]
    return 0

init()
