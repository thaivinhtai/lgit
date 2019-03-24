"""config the commit user."""

from .tools import add_content_file, get_args


def execute_config(repo, user):
    """
    execute_config(repo) -> config the user.

    Required argument:
        repo    -- path of repository.
        user    -- user'a name.
    """
    args = get_args()[2:]
    if len(args) < 2:
        return 0
    if args[0] == "--author":
        return add_content_file(repo + "/.lgit/config", user)
    return 0
