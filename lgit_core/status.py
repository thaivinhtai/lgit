"""This module displays paths that have differences between the index file and
the current HEAD commit, paths that have differences between the working tree
and the index file, and paths in the working tree that are not tracked by LGit
(and are not ignored by gitignore(5)). The first are what you would commit by
running git commit; the second and third are what you could commit by running
git add before running git commit..
"""

from .tools import get_all_file


def update_status():
    """
    update_status() -> show the working tree status.
    """
