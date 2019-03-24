"""This module is a very light version of git add command, which will store a
copy of the file content in the lgit database.

File contents will be stored in the lgit database with thier SHA hash value.
"""

from os.path import exists
from os import mkdir
from .tools import (get_args, get_full_path, call_subprocess, get_file_type,
                    add_content_file, get_hash, read_file, check_arg,
                    get_all_file, check_index, prepair_for_register)


def register_to_index(file, repo, hash_value):
    """
    register_to_index(file) ->  register to index file in lgit database.

    Required argument:
        file           --  file name.
        repo           --  the folder contain lgit database.
        hash_value     --  a hash value for register in index file.
    """
    file_timestamp, path_file, index_content = prepair_for_register(file, repo)
    registered, index = check_index(path_file, index_content)
    if not registered:
        index_content.append(file_timestamp + " " + hash_value + " " +
                             hash_value + " " * 42 + path_file)
    else:
        index_content[index] = index_content[index].\
                               replace(index_content[index][:96],
                                       (file_timestamp + " " + hash_value +
                                        " " + hash_value))
    while "" in index_content:
        index_content.remove("")
    content_to_write = ""
    for element in index_content:
        content_to_write += element + "\n"
    return add_content_file(repo + "/.lgit/index", content_to_write)


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
        objects_folder = repo_path + "/.lgit/objects/" + folder
        if not exists(objects_folder):
            mkdir(objects_folder)
        return add_content_file(objects_folder + "/" + file_name, file_content)

    def create_object_file(file):
        """
        create_object_file(file)    -> create file in objects directoy.

        Required argument:
            file    --  file name.
        """
        hash_value = get_hash(get_full_path(file))
        folder = hash_value[0:2]
        file_name = hash_value[2:]
        file_content = read_file(get_full_path(file))
        register_to_index(file, repo_path, hash_value)
        return create_file(folder, file_name, file_content)

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

    doc = '/lgit-docs/Manual page lgit-add(1)'
    current_dir = get_args()[0][:len(get_args()[0]) - 8]
    args = list(get_args()[2:])

    if not args:
        return print("Nothing specified, nothing added.",
                     "Maybe you wanted to say 'lgit add .'?", sep='\n')

    if args[0] == "--help":
        return call_subprocess(current_dir + doc)
    if "-help" in args or "-h" in args:
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
