"""This module is a very light version of git add command, which will store a
copy of the file content in the lgit database.

File contents will be stored in the lgit database with thier SHA hash value.
"""

from os.path import exists, join
from os import mkdir, walk
from .tools import (get_args, get_full_path, call_subprocess,
                    get_file_type, add_content_file,
                    get_hash, read_file)


def add(file, repo_path):
    """
    add(file)   ->  store a copy of the file content in the lgit database.

    Required argument:
        file        --  a file's path specification.
        repo_path   --  path of lgit repo.
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
        objects_folder = repo_path + ".lgit/objects/" + folder
        if not exists(objects_folder):
            mkdir(objects_folder)
        return add_content_file(objects_folder + "/" + file_name, file_content)

    def create_object_file(file):
        """
        create_object_file(file)    -> create file in objects directoy.

        Required argument:
            file    --  file name.
        """
        folder = get_hash(get_full_path(file))[0:2]
        file_name = get_hash(get_full_path(file))[2:]
        file_content = read_file(get_full_path(file))
        create_file(folder, file_name, file_content)

    def get_all_file(directory):
        """
        get_all_file(directory)  ->  find all the file in dir and subdir.

        This function return a list of all path of files in the dirctory and
        its children.

        Required argument:
            directory   -- path of directory
        """
        files_list = []
        for direc, subdir, files in walk(directory):
            del subdir
            files_list.extend([join(direc, file) for file in files])
        files_list = filter(lambda data: '/.lgit' not in data, files_list)
        return files_list

    # Check if file is directoy or a plain file
    if get_file_type(file) == "file":
        return create_object_file(file)
    if get_file_type(file) == "directory":
        files_list = get_all_file(get_full_path(file))
        return [create_object_file(file) for file in files_list]


def execute_add(repo_path):
    """
    execute_add()   -> execute lgit add command, this is main of this module.

    Execute function of this module with error handling.

    required argument:
        repo_path   --  path of lgit repository.
    """

    def check_arg(args, repo_path):
        """
        check_arg(args) ->  check all argument in args.

        This function check all argument in args (list of arguments), if there
        is an unvalid argument, return False.

        Required argument:
            args        --  list of arguments.
            repo_path   --  path of lgit repository.
        """
        split_repo_path = repo_path.split("/")
        del split_repo_path[-1]
        str_repo = str(split_repo_path)[:len(split_repo_path) - 1]
        index = -1
        for element in args:
            index += 1
            split_element = get_full_path(element).split("/")
            if str_repo not in str(split_element):
                return index, False, 2
            if not exists(get_full_path(element)):
                return index, False, 1
        return index, True, 0

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

    index, check, error = check_arg(args, repo_path)
    if check is False and error == 1:
        return print("fatal: pathspec '" + args[index] + "' did not",
                     "match any files")
    if check is False and error == 2:
        return print("fatal:", args[index] + ":", "'" + args[index] + "'",
                     "is outside repository")
    for element in args:
        add(get_full_path(element), repo_path)
    return 0
