"""This module is seen as a constructor of the directory and marks it as a
Python package. This module also contain some stuff to help the project easier
to develop."""

from .init import execute_init
from .add import execute_add
from .status import execute_status
from .log import execute_log
from .rm import execute_rm
from .config import execute_config
from .commit import execute_commit
