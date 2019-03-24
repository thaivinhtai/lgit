from .tools import (get_args, add_content_file, read_file)
from os import environ
from time import strftime, localtime, time


def execute_commit(repo_path):
    """
    execute_commit()   -> execute lgit commit command, this is main
                        of this module.

    Execute function of this module with error handling.

    required argument:
        repo_path   --  path of lgit repository.
    """
    # Create argurments
    args = get_args()[3:]
    commit_mess = args[0]
    current_time = time()
    fcurrent_time = strftime('%Y%m%d%H%M%S',
                             localtime(current_time))
    index_content = read_file(repo_path + "/.lgit/index").split('\n')
    index_content.remove("")
    config_content = read_file(repo_path + "/.lgit/config").split('\n')
    config_content.remove("")
    print(config_content)
    # Loop all available added files in stage area
    index = -1
    for line in index_content:
        index += 1
        # This is file name of commit file and snapshot file
        file_name = line[:14]
        # This is full path of these two files
        commit_file = repo_path + "/.lgit/commits/" + file_name
        snap_file = repo_path + "/.lgit/snapshots/" + file_name
        # This is content of these two files
        commit_content = config_content[0] + "\n" + str(fcurrent_time) +\
            "\n\n" + commit_mess + "\n"
        print(commit_content)
        snap_content = line[56:96] + line[137:]
        # Add content to these two files
        add_content_file(commit_file, commit_content)
        add_content_file(snap_file, snap_content)
        # Add committed index to stage area
        index_content[index] = index_content[index].\
            replace(index_content[index][97:], snap_content)

    content_to_write = ""
    for element in index_content:
        content_to_write += element + "\n"
    return add_content_file(repo_path + "/.lgit/index", content_to_write)
