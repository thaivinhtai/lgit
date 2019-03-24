"""Remove files from the index, or from the working tree and the index. git rm
will not remove a file from just your working directory. (There is no option to
remove a file only from the working tree and yet keep it in the index;
use /bin/rm if you want to do that.) The files being removed have to be
identical to the tip of the branch, and no updates to their contents can be
staged in the index, though that default behavior can be overridden with
the -f option. When --cached is given, the staged content has to match either
the tip of the branch or the file on disk, allowing the file to be removed from
just the index.
"""

from os import remove, rmdir
from .tools import get_args, check_arg, get_file_type, add_content_file


def execute_rm(repo):
    """
    execute_rm(repo) -> Remove files from the working tree and from the index.

    Required argument:
        repo    --  path of repository.
    """
    args = get_args()[2:]
    if not args:
        return print("usage: lgit rm <file>...")
    index, check, error = check_arg(args, repo_path)
    if check is False and error == 1:
        return print("fatal: pathspec '" + args[index] + "' did not",
                     "match any files")
    if check is False and error == 2:
        return print("fatal:", args[index] + ":", "'" + args[index] + "'",
                     "is outside repository")
    index_content = read_file(repo + "/.lgit/index").split('\n')
    for file in args:
        if get_file_type(file) == "directoy":
            file = get_full_path(file).replace(repo, "")
            for line in index_content:
                if file in line:
                    index_content.remove(file)
            rmdir(file)
        if get_file_type(file) == "file":
            file = get_full_path(file).replace(repo, "")
            for line in index_content:
                if file in line:
                    index_content.remove(file)
            remove(file)
    while '' in index_content:
        index_content.remove('')
    content = ""
    for line in index_content:
        content += line + '\n'
    return add_content_file(repo + "/.lgit/index", content)
