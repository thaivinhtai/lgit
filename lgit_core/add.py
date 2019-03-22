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
        objects_folder = objects_path + folder
        if not exists(objects_folder):
            mkdir(objects_folder)
        return add_content_file(objects_folder + "/" + file_name, file_content)

    def add_recursion(list_file):
        """
        add_recursion(list_file)    ->  recur the function add.

        Required argument:
            list_file   -> list of files.
        """
        for element in list_file:
            add(element, object_path)
        return 0

    # Check if file is directoy or a plain file
    if get_file_type(file) == "file":
        folder = get_hash(get_full_path(file))[0:2]
        file_name = get_hash(get_full_path(file))[2:]
        file_content = read_file(get_full_path(file))
        return create_file(folder, file_name, file_content)
    elif get_file_type(file) == "directory":
        return add_recursion(list_files(file))


def execute_add():
    """
    execute_add()   -> execute lgit add command, this is main of this module.

    Execute function of this module with error handling.
    """
    
