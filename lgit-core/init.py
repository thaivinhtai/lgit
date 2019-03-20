"""This module simulates a very small concept of "git init" command, which will
create a "lgit repository" via make a specified directory.

Functions in this module:
    -   .....
    -   init(path)
"""

from tools import *


def init(path=''):
    """
    init(path)  -> adfsadtwh
    """
    folders = [
    '.lgit',
    '.lgit/object',
    '.lgit/commits',
    '.lgit/snapshots'
    ]
    [mkdir(path + folder) for folder in folders]

init()
