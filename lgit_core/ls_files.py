"""lists all the files currently tracked in the index, relative to the current
directory"""

from .tools import read_file


def execute_lls_files(repo):
    """
    execute_lls_files(repo) -> list all file.

    Required argument:
        repo    -- path of repository.
    """
    list_file = read_files(repo + "/.lgit/index").split("\n")[138:]
    print(*list_file, sep='\n')
