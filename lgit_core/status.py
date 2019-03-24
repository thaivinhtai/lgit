"""This module displays paths that have differences between the index file and
the current HEAD commit, paths that have differences between the working tree
and the index file, and paths in the working tree that are not tracked by LGit
(and are not ignored by lgitignore(5)). The first are what you would commit by
running git commit; the second and third are what you could commit by running
git add before running git commit..
"""

from .tools import (get_all_file, get_full_path, read_file, get_hash,
                    get_timestamp, call_subprocess, check_arg, get_args,
                    get_file_type, prepair_for_register, check_index,
                    add_content_file)


def get_status(file, repo_path):
    """
    get_status() -> get status of file.

    Required argument:
        file        --  file need to update status.
        repo_path   --  path of repository.
    """
    file_timestamp, path_file, index_content = prepair_for_register(file,
                                                                    repo_path)
    registered, index = check_index(path_file, index_content)
    hash_value = get_hash(get_full_path(file))
    content_to_write = ""
    print(registered)
    if not registered:
        return "untracked"
    index_content[index] = index_content[index].\
        replace(index_content[index][:55],
                (file_timestamp + " " + hash_value))
    while "" in index_content:
        index_content.remove("")
    content_to_write = ""
    for element in index_content:
        content_to_write += element + "\n"
    add_content_file(repo_path + "/.lgit/index", content_to_write)
    if index_content[index][15:55] == index_content[index][97:137]:
        return "commited"
    if index_content[index][97:137] == " " * 40:
        return "added"
    if index_content[index][15:55] != index_content[index][56:96]:
        return "not staged"
    return "modified"


def execute_status(repo_path):
    """
    execute_status(repo_path) -> Show the working tree status.

    Required argument:
        repo_path   --  path of repository.
    """

    def classify_file(args):
        """
        classify_file(args)  -> return list of same type file.

        Required argument:
            args --  list of files.
        """
        files = []
        directories = []
        for element in args:
            element = get_full_path(element)
            if get_file_type(element) == "file":
                files.append(element)
            elif get_file_type(element) == "directory":
                directories.append(element)
        return files, directories

    def classify_status(files):
        """
        classify_status(files)  ->  returns lists of files have same status.

        Required argument:
            files   --  list of files.
        """
        untracked = []
        commited = []
        modified = []
        added = []
        not_staged = []
        for file in files:
            if get_status(file, repo_path) == "untracked":
                untracked.append(file)
            elif get_status(file, repo_path) == "commited":
                commited.append(file)
            elif get_status(file, repo_path) == "modified":
                modified.append(file)
            elif get_status(file, repo_path) == "added":
                added.append(file)
            elif get_status(file, repo_path) == "not staged":
                not_staged.append(file)
        return untracked, commited, modified, added, not_staged

    doc = '/lgit-docs/Manual page lgit-status(1)'
    current_dir = get_args()[0][:len(get_args()[0]) - 8]
    args = list(get_args()[2:])
    if not args:
        args = ["."]
    if args[0] == "--help":
        return call_subprocess(current_dir + doc)
    if "-help" in args or "-h" in args:
        return print("usage: git status <pathspec>")
    index, check, error = check_arg(args, repo_path)
    if check is False and error == 2:
        return print("fatal:", args[index] + ":", "'" + args[index] + "'",
                     "is outside repository")
    if check is False and error == 1:
        args.remove(args[index])
    files, directories = classify_file(args)
    for element in directories:
        files += get_all_file(element)
    untracked, commited, modified, added, not_staged = classify_status(files)
    if not untracked and not added and not modified and not not_staged and\
       commited:
        return print("On branch master\n\
                     nothing to commit, working directory clean")
    print("On branch master\n")
    print("No commits yet\n")
    if added or modified:
        print("Changes to be commited:")
        print('\t(use "./lgit.py reset HEAD ..." to unstage)\n')
        for file in modified:
            print('\t\tmodified:', file.replace(repo_path, ""))
        for file in added:
            print('\t\tnew file:', file.replace(repo_path, ""))
        print("")
    if not_staged:
        print("Changes not staged for commit:")
        print('\t(use "./lgit.py add ..." to update what will be committed)')
        print('\t(use "./lgit.py checkout -- ..." to discard changes in'
              'working directory)\n')
        for file in not_staged:
            print('\t\tmodified:', file.replace(repo_path, ""))
        print("")
    if untracked:
        print("Untracked files:")
        print('\t(use "./lgit.py add <file>..." to include in what will be',
              'committed)\n')
        for file in untracked:
            print('\t\t', file.replace(repo_path, ""))
        print("")
        print("nothing added to commit but untracked files present",
              '(use "./lgit.py add" to track)')
    return 0
