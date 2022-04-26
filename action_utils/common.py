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


def _get_repo_name_from_url(url: str) -> str:
    """Given a https/git url, get the repository name

    :param url: The url to parse, either https://github.com/... or git@github.com:...
    :return: The repository name parsed from the url
    """
    return url.split('.git')[0].split('/')[-1]


def get_repo_name(git_repo: git.repo.base.Repo) -> str:
    """Given a GitPython Repo object, determine the name of the repository based on the remote

    :param git_repo: The Repo instance
    :return: The name of the repository
    """
    return _get_repo_name_from_url(git_repo.remotes.origin.url)


def get_submodule_name(git_submodule: git.Submodule) -> str:
    """Given a GitPython Submodule object, determine the name of the submodule based on the remote

    :param git_submodule: The Submodule instance
    :return: The name of the repository
    """
    return _get_repo_name_from_url(git_submodule.url)
