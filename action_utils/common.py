"""Constants, classes, and utilities related to git/GitHub common across scripts"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import git

GENAPSYS_GITHUB = "GenapsysInc"

APPROVED = "APPROVED"
COMMENTED = "COMMENTED"
CHANGES_REQUESTED = "CHANGES_REQUESTED"


class ConfigurationError(Exception):
    """Should be raised when input arguments are found to be incorrect/invalid"""


def get_repo_name_from_url(url: str) -> str:
    """Given a https/git url, get the repository name

    :param url: The url to parse, either https://github.com/... or git@github.com:...
    :return: The repository name parsed from the url
    """
    return url.split(".git")[0].split("/")[-1]


def get_repo_name(git_repo: git.repo.base.Repo) -> str:
    """Given a GitPython Repo object, determine the name of the repository based on the remote

    :param git_repo: The Repo instance
    :return: The name of the repository
    """
    return get_repo_name_from_url(git_repo.remotes.origin.url)


def get_submodule_name(git_submodule: git.Submodule) -> str:
    """Given a GitPython Submodule object, determine the name of the submodule based on the remote

    :param git_submodule: The Submodule instance
    :return: The name of the repository
    """
    return get_repo_name_from_url(git_submodule.url)


def a_function_to_show_code_coverage(int1: int, int2: int) -> int:
    """Adds 2 ints together!

    :param int1: The first int
    :param int2: The second int
    :return: The sum of the ints
    """
    print(f"Adding {int1} and {int2} together!")

    return int1 + int2
