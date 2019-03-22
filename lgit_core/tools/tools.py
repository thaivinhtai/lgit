"""This module provides some aliases that will be used many times in the "lgit"
program.

Functions in this module:
    -   get_full_path(file) -> return full path of file.
    -   get_file_type(file) -> return type of file.
    -   read_file(file) ->  return content of a file.
    -   print_file(file)    -> print the content of file to console.
    -   get_args()  -> return a list of arguments.
    -   call_subprocess(option, subprocess) -> call the subprocess.
    -   list_dir(dir)   ->  return all files in a directory.
    -   add_content_file(name, content)  -> add content to a file.
    -   hash_file(file) -> hash file.
"""

from os import path, open, close, write, O_RDWR, O_CREAT, fdopen, listdir
from sys import argv
from subprocess import run
from hashlib import sha1


def get_full_path(file):
    """
    get_full_path(file) -> return full path of file.

    This function figures out exactly the path of file on system.

    Required argument:
        file    --  a string-type file name.
    """
    if file[0] == '~':
        file = path.expanduser(file)
    else:
        file = path.realpath(file)
    return file


def get_file_type(file):
    """
    get_file_type(file) -> return type of file.

    This function check if a file is a directory, file and return its type via
    a string. If the file is not exist, return None.

    Required argument:
        file    -- a string-type file name.
    """
    try:
        file = get_full_path(file)
        if path.isfile(file):
            return "file"
        if path.isdir(file):
            return "directory"
        return 0
    except FileNotFoundError:
        return None


def read_file(file):
    """
    read_file(file)     ->  get content of a file.

    Required argument:
        file    --  name or path of file.
    """
    try:
        file = get_full_path(file)
        file = open(file, O_RDWR)
        file = fdopen(file)
        content = file.read()
        file.close()
        return content
    except (UnicodeDecodeError, PermissionError) as error:
        return ""


def print_file(file):
    """
    print_file(file)    -> print the content of file to console.

    Required argument:
        file    -> name of file need to print content.
    """
    content = read_file(file)
    return print(content)


def get_args():
    """
    get_args()  -> return a list of arguments.

    Get arguments from console for processing.
    """
    return argv


def call_subprocess(file, subprocess='less'):
    """
    call_subprocess(option, subprocess) -> call the subprocess.

    Required arguments:
        - file          -- file want to open in subprocess.
        - subprocess    -- name of process, defaul is less.
    """
    file = get_full_path(file)
    return run([subprocess, file])


def list_files(dir):
    """
    list_dir(dir)   ->  return all files in a directory.

    Required argument:
        dir     -- name of directory.
    """
    try:
        return listdir(get_full_path(dir))
    except (NotADirectoryError, FileNotFoundError) as error:
        return []


def add_content_file(name, content=""):
    """
    add_content_file(name, content)  -> add content to a file.

    This function add content to a file, if it's not exist, create it.

    Required arguments:
        name        -- name of file.
        content     -- content add to file.
    """
    file_descriptor = open(name, O_RDWR | O_CREAT, 0o644)
    byte_object = str.encode(content)
    ret = write(file_descriptor, byte_object)
    return close(file_descriptor)


def get_hash(file):
    """
    get_hash(file)  -> return hash value of file.

    This function return SHA1 hash value of file.

    Required argument:
        file    --  a file need to be hashed.
    """
    content = read_file(file)
    return sha1(content.encode()).hexdigest()
