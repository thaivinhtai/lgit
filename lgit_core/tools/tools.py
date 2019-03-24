"""This module provides some aliases that will be used many times in the "lgit"
program.

Functions in this module:
    -   get_full_path(file) -> return full path of file.
    -   get_file_type(file) -> return type of file.
    -   read_file(file) ->  return content of a file.
    -   open_file(file) ->  open a file to read and write.
    -   print_file(file)    -> print the content of file to console.
    -   get_args()  -> return a list of arguments.
    -   call_subprocess(option, subprocess) -> call the subprocess.
    -   list_dir(dir)   ->  return all files in a directory.
    -   add_content_file(name, content)  -> add content to a file.
    -   hash_file(file) -> hash file.
    -   get_timestamp(file) -> return timestamp of file.
    -   get_all_file(directory)  ->  find all the file in dir and subdir.
    -   check_index(path_file, index_content) -> check if file had registred.
    -   prepair_for_register(file, repo) -> return data for registering.
    -   check_arg(args) ->  check all argument in args.
"""

from os import path, open, close, write, O_RDWR, O_CREAT, fdopen, listdir, walk
from os.path import join, exists
from time import strftime, localtime
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


def open_file(file):
    """
    open_file(file) ->  open a file for reading and writing.

    This function returns a file object.

    Required argument:
        file    --  file' name.
    """
    try:
        file = get_full_path(file)
        file = open(file, O_RDWR)
        file = fdopen(file)
        return file
    except PermissionError:
        return None


def read_file(file):
    """
    read_file(file)     ->  get content of a file.

    Required argument:
        file    --  name or path of file.
    """
    try:
        file = open_file(file)
        content = file.read()
        file.close()
        return content
    except (UnicodeDecodeError, PermissionError, AttributeError) as errors:
        del errors
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


def list_files(directoy):
    """
    list_dir(dir)   ->  return all files in a directory.

    Required argument:
        directoy     -- name of directory.
    """
    try:
        return listdir(get_full_path(directoy))
    except (NotADirectoryError, FileNotFoundError) as error:
        del error
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
    write(file_descriptor, byte_object)
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


def get_timestamp(file):
    """
    get_timestamp(file) ->  return timestamp of file.

    This function returns timestamp of file via a string.

    Required argument:
        file    --  file's name.
    """
    file = get_full_path(file)
    mod_time_since_epoc = path.getmtime(file)
    modification_time = strftime('%Y%m%d%H%M%S',
                                 localtime(mod_time_since_epoc))
    return modification_time


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


def check_index(path_file, index_content):
    """
    check_index(path_file, index_content) -> check if file had registred.

    This function check a file had already in index or not. Return False
    if not, else return True and line index contain file.

    Required argument:
        path_file       --  path of file.
        index_content   --  content of index file.
    """
    registered = False
    index = -1
    for line in index_content:
        index += 1
        if path_file in line:
            registered = True
            break
    return registered, index


def prepair_for_register(file, repo):
    """
    prepair_for_register(file, repo) -> return data for registering.

    This function returns timestamp, hash, content in index file.

    Required argument:
        file    --  file name need to get timestamp, hash.
        repo    --  path of repository.
    """
    full_path_file = get_full_path(file)
    file_timestamp = get_timestamp(file)
    path_file = full_path_file.replace(repo + "/", '')
    index_content = read_file(repo + "/.lgit/index").split('\n')
    if len(index_content) == 1 and index_content[0] == '':
        index_content = []
    return file_timestamp, path_file, index_content


def check_arg(args, repo_path):
    """
    check_arg(args) ->  check all argument in args.

    This function check all argument in args (list of arguments), if there
    is an unvalid argument, return False.

    Required argument:
        args        --  list of arguments.
        repo_path   --  path of lgit repository.
    """
    index = -1
    for element in args:
        index += 1
        if repo_path not in get_full_path(element):
            return index, False, 2
        if not exists(get_full_path(element)):
            return index, False, 1
    return index, True, 0
