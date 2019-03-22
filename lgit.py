#!/usr/bin/env python3

"""This is main module of Lgit program, which is a simple simulation of git."""

from os import getcwd
from lgit_core import (execute_init, execute_add)
from lgit_core.tools import get_args, list_files


def find_repo():
    """
    find_repo() -> find lgit repository.
    """

    def check_path(folder, track):
        """
        check_path(folder, track) ->  check the current directory.

        This function check if there is a lgit repository in the path.

        Required argument:
            folder  --  current directory's name.
            track   --  current directory pathspec.
        """
        repo = ""
        if ".lgit" in list_files(track):
            repo = track
        return repo

    current_dir = getcwd().split("/")
    current_dir.remove('')
    repo = ""
    track = ""
    for element in current_dir:
        track += "/" + element
        repo = check_path(element, track)
    return repo + "/"


def call_init():
    """
    call_init() -> execute the lgit init command.
    """
    return execute_init()


def call_add():
    """
    call_add()  -> execute the lgit add command and handle some error.
    """
    if find_repo() != "/":
        return execute_add(find_repo())



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
    func = switcher.get(command, None)
    return func()


def main():
    """
    This is main function.
    """
    args = list(get_args())
    if len(args) > 1:
        args.remove(args[0])
    args = args[0]
    switch_command(args)


if __name__ == "__main__":
    main()
