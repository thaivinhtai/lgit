#!/usr/bin/env python3

"""This is main module of Lgit program, which is a simple simulation of git."""

from os import getcwd
from lgit_core import (execute_init, execute_add)
from lgit_core.tools import get_args, list_files, print_file


def find_repo():
    """
    find_repo() -> find lgit repository.
    """

    def check_path(track, repo):
        """
        check_path(folder, track) ->  check the current directory.

        This function check if there is a lgit repository in the path.

        Required argument:
            track   --  current directory pathspec.
            repo    --  folder contain .lgit.
        """
        if ".lgit" in list_files(track):
            repo = track
        return repo

    current_dir = getcwd().split("/")
    current_dir.remove('')
    repo = ""
    track = ""
    for element in current_dir:
        track += "/" + element
        repo = check_path(track, repo)
    return repo


def call_init():
    """
    call_init() -> execute the lgit init command.
    """
    return execute_init()


def call_add():
    """
    call_add()  -> execute the lgit add command and handle some error.
    """
    if find_repo() != "":
        return execute_add(find_repo())
    return print("fatal: not a git repository",
                 "(or any of the parent directories)")


def switch_command(command):
    """
    switch_command(command) ->  choose a command.

    This is a manual swithcer for select function quickly.

    Required arguments:
        command     --  a string-type, which is name of command.
    """

    switcher = {
        'init': call_init,
        'add': call_add
    }
    try:
        func = switcher.get(command, None)
        return func()
    except IndexError:
        print("lgit: '" + command + "' is not a lgit command.",
              "See 'lgit --help'.")


def main():
    """
    This is main function.
    """
    try:
        command = get_args()[1]
        return switch_command(command)
    except IndexError:
        current_dir = get_args()[0][:len(get_args()[0]) - 8]
        doc = '/lgit-docs/lgit-help'
        print_file(current_dir + doc)


if __name__ == "__main__":
    main()
