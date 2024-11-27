"""Private utils functions for reading files."""

# Citation: get_path is from: https://github.com/sktime/sktime/blob/v0.34.0/sktime/datasets/_readers_writers/utils.py

__authors__ = ["RobotPsychologist"]

__all__ = [
    "get_path",
]

import os
import pathlib
import textwrap
from typing import Union

def get_path(path: Union[str, pathlib.Path], suffix: str) -> str:
    """Automatic inference of file ending in data loaders for single file types.

    This function checks if the provided path has a specified suffix. If not,
    it checks if a file with the same name exists. If not, it adds the specified
    suffix to the path.

    Parameters
    ----------
    path: str or pathlib.Path
        The full pathname or filename.
    suffix: str
        The expected file extension.

    Returns
    -------
    resolved_path: str
        The filename with required extension
    """
    p_ = pathlib.Path(path).expanduser().resolve()
    resolved_path = str(p_)

    # Checks if the path has any extension
    if not p_.suffix:
        # Checks if a file with the same name exists
        if not os.path.exists(resolved_path):
            # adds the specified extension to the path
            resolved_path += suffix
    return resolved_path


def get_root_dir(current_dir=None):
    '''
    Get the root directory of the project by looking for a specific directory
    (e.g., '.github') that indicates the project root.

    Parameters
    ----------
    current_dir : str, optional
        The starting directory to search from. If None, uses the current working directory.

    Returns
    -------
    str
        The root directory of the project.
    '''
    if current_dir is None:
        current_dir = os.getcwd()

    # Directory that uniquely identifies the root
    unique_dir = '.github'

    while current_dir != os.path.dirname(current_dir):
        if os.path.isdir(os.path.join(current_dir, unique_dir)):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError(f"Project root directory not found. '{unique_dir}' directory missing in path.")
