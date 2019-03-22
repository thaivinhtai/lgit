#!/usr/bin/env python3

"""This is main module of Lgit program, which is a simple simulation of git."""

from os import getcwd
from lgit_core import (execute_init, execute_add)
from lgit_core.tools import get_args, list_files


def switch_command(command):
    """
    switch_command(command) ->  choose a command.

    This is a manual swithcer for select function quickly.

    Required arguments:
        command     --  a string-type, which is name of command.
    """

    switcher = {
        'init': execute_init,
        'add': execute_add
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
    if args[0] == "init":
        return switch_command(args[0])
    current_dir = getcwd().split("/")
    repo = ""
    track = ""
    for element in current_dir:
        track = track + "/" + element

    return switch_command(args[0])
    print(current_dir)


if __name__ == "__main__":
    main()
