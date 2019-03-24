"""This module is a very light version of git add command, which will store a
copy of the file content in the lgit database.

File contents will be stored in the lgit database with thier SHA hash value.
"""

from os.path import exists
from os import mkdir
from .tools import (get_args, get_full_path, call_subprocess,
                    get_file_type, list_files, add_content_file,
                    get_hash, read_file)


def add(file, objects_path):
    """
    add(file)   ->  store a copy of the file content in the lgit database.

    Required argument:
        file    ->  a file's path specification.
    """

    def create_file(folder, file_name, file_content):
        """
        create_file(folder, file_name, file_content) -> create file in folder.

        This function create file and fill with content in a folder. If folder
        does not exist, create it.

        Required arguments:
            folder          --  folder name.
            file_name       --  file's name.
            file_content    --  content of file.
        """
        objects_folder = objects_path + ".lgit/objects/" + folder
        # print(objects_folder)
        if not exists(objects_folder):
            mkdir(objects_folder)
        return add_content_file(objects_folder + "/" + file_name, file_content)

    def add_recursion(files):
        """
        add_recursion(list_file)    ->  recur the function add.

        Required argument:
            list_file   -> list of files.
        """
        # print(files)
        for file in files:
            # print(get_full_path(file))
            add(get_full_path(file), objects_path)
        return 0

    def skip_repo(file):
        """
        skip_repo(file)   ->  remove ".lgit" in list.

        This function check if there are repository in a directoy, skip it.

        Required aegument:
            file    -- a directory's name.
        """
        files = list(list_files(file))
        if ".lgit" in files:
            files.remove(".lgit")
        return files

    def create_object_file():
        """
        create_object_file()    -> create file in objects directoy.
        """
        folder = get_hash(get_full_path(file))[0:2]
        file_name = get_hash(get_full_path(file))[2:]
        file_content = read_file(get_full_path(file))
        create_file(folder, file_name, file_content)

    # Check if file is directoy or a plain file
    if get_file_type(file) == "file":
        # print(file)
        return create_object_file()
    if get_file_type(file) == "directory":
        files = list(skip_repo(file))
        print(file)
        print(files)
        return add_recursion(files)


def execute_add(objects_path):
    """
    execute_add()   -> execute lgit add command, this is main of this module.

    Execute function of this module with error handling.
    """

    def check_arg(args):
        """
        check_arg(args) ->  check all argument in args.

        This function check all argument in args (list of arguments), if there
        is an unvalid argument, return False.

        Required argument:
            args    --  list of arguments.
        """
        index = 0
        for element in args:
            index += 1
            if not exists(get_full_path(element)):
                return index, False
        return index, True

    doc = '/lgit-docs/Manual page lgit-add(1)'
    current_dir = get_args()[0][:len(get_args()[0]) - 8]
    args = list(get_args()[2:])

    if not args:
        return print("Nothing specified, nothing added.",
                     "Maybe you wanted to say 'lgit add .'?", sep='\n')
    if args[0] == "--help":
        return call_subprocess(current_dir + doc)
    if "-help" in args or "--help" in args:
        return print("usage: git add <pathspec>")

    index, check = check_arg(args)
    if check is False:
        return print("fatal: pathspec '" + args[index] + "' did not",
                     "match any files")
    for element in args:
        add(get_full_path(element), objects_path)
    return 0
