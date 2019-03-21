"""This module simulates a very small concept of "git init" command, which will
create a "lgit repository" via make a specified directory.

Functions in this module:
    -   .....
    -   init(path)  ->  create a "lgit repository".
"""

from os import mkdir, environ
from .tools import (get_args, get_full_path, call_subprocess,
                    get_file_type, list_files, add_content_file)


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

    return ([mkdir(path + folder) for folder in folders],
            add_content_file(".lgit/index"),
            add_content_file(".lgit/config", environ['LOGNAME'] + '\n'))


def execute_init():
    """
    execute_init() -> execute init, this is main function of this module.

    Execute the function of this module with except handling.
    """
    args = get_args()[2:]
    if not args:
        args.append('.')

    if len(args) > 1 or "-h" in args:
        return print("usage: git init [<directory>]")
    if "--help" in args:
        return call_subprocess('./lgit-docs/Manual page lgit-init(1)')

    if ".lgit" in list_files(args[0]):
        return print("Reinitialized existing Lgit repository in",
                     get_full_path(args[0]) + "/.lgit/")

    if get_file_type(args[0]) != "file":
        print("Initialized empty legalit repository in",
              get_full_path(args[0]) + "/.lgit/")
        return init(args[0] + "/")
    return print("fatal: cannot mkdir", args[0], ": File exists")
