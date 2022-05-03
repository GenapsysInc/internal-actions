"""Constants, classes, and utilities related to git/GitHub common across scripts"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from functools import total_ordering
import re

import git

GENAPSYS_GITHUB = "GenapsysInc"

APPROVED = "APPROVED"
COMMENTED = "COMMENTED"
CHANGES_REQUESTED = "CHANGES_REQUESTED"

VERSION_RELEASE_DELIM = "-"
VERSION_MAJOR_MINOR_PATCH_DELIM = "."
VERSION_TAG_REGEX = re.compile(r"\d+\.\d+\.\d+-\d+")


class ConfigurationError(Exception):
    """Should be raised when input arguments are found to be incorrect/invalid"""


class InvalidVersion(Exception):
    """Should be raised when parsing a tag that does not conform to expected version format"""


@total_ordering
class VersionTag:
    """Representation of a git tag in the form of major.minor.patch-release"""

    def __init__(self, tag: str):
        """Ctor.

        :param tag: Tag string in "major.minor.patch-release" format
        """
        # Will be set by setting self.tag
        self.__major = None
        self.__minor = None
        self.__patch = None
        self.__release = None

        self.tag = tag

    def __str__(self):
        return self.tag

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major

        if self.minor != other.minor:
            return self.minor < other.minor

        if self.patch != other.patch:
            return self.patch < other.patch

        # If we got this far then major, minor, and patch are identical
        return False

    @property
    def tag(self) -> str:
        """The tag string"""
        return self.__tag

    @tag.setter
    def tag(self, new_tag: str):
        """Assert valid format, store the given tag, and determine major, minor, patch, and release numbers"""
        try:
            self.__tag = re.match(VERSION_TAG_REGEX, new_tag).group()
        except AttributeError as attr_error:
            raise InvalidVersion(f"{new_tag} did not conform to major.minor.patch-release format") from attr_error

        major_minor_patch, release = self.tag.split(VERSION_RELEASE_DELIM)
        major, minor, patch = major_minor_patch.split(VERSION_MAJOR_MINOR_PATCH_DELIM)

        self.__major = int(major)
        self.__minor = int(minor)
        self.__patch = int(patch)
        self.__release = int(release)

    @property
    def major(self) -> int:
        """The major version number"""
        return self.__major

    @property
    def minor(self) -> int:
        """The minor version number"""
        return self.__minor

    @property
    def patch(self) -> int:
        """The patch version number"""
        return self.__patch

    @property
    def release(self) -> int:
        """The release number"""
        return self.__release

    def get_new_release(self) -> str:
        """Return a new tag with the release number incremented by 1

        :return: The new tag string
        """
        return f"{self.major}.{self.minor}.{self.patch}-{self.release + 1}"


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
