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

    def create_unexisted_dir(directory, element):
        """
        create_unexisted_dir(directory, element)-> create unexisted directory.

        This function create directory if there are unexisted directory in the
        path.

        Required argument:
            directory    --     a full path of directory.
            element      --     a directory's name.
        """
        directory = directory + "/" + element
        if get_file_type(directory) == 0:
            mkdir(directory)
        return directory

    path = path.split("/")
    path[0] = "/"
    directory = ""
    for element in path[1:]:
        directory = create_unexisted_dir(directory, element)
    folders = ['.lgit', '.lgit/objects', '.lgit/commits', '.lgit/snapshots']

    return ([mkdir(directory + "/" + folder) for folder in folders],
            add_content_file(directory + "/" + ".lgit/index"),
            add_content_file(directory + "/" + ".lgit/config",
                             environ['LOGNAME'] + '\n'))


def execute_init():
    """
    execute_init() -> execute init, this is main function of this module.

    Execute the function of this module with except handling.
    """
    # path of manual of init.
    doc = '/lgit-docs/Manual page lgit-init(1)'
    current_dir = get_args()[0][:len(get_args()[0]) - 8]
    args = get_args()[2:]
    if not args:
        args.append('.')
    # If there are more than one argument
    if len(args) > 1 or "-h" in args:
        return print("usage: git init [<directory>]")
    # If there is "--help" in arguments
    if "--help" in args:
        return call_subprocess(current_dir + doc)
    # If there is already have .lgit in directory
    if ".lgit" in list_files(get_full_path(args[0])):
        return print("Reinitialized existing Lgit repository in",
                     get_full_path(args[0]) + "/.lgit/")
    # Create .lgit
    if get_file_type(get_full_path(args[0])) != "file":
        print("Initialized empty Lgit repository in",
              get_full_path(args[0]) + "/.lgit/")
        init(get_full_path(args[0]))
        return get_full_path(args[0]) + "/.lgit/objects/"
    return print("fatal: cannot mkdir", args[0], ": File exists")
