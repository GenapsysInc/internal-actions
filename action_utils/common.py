"""Constants, classes, and utilities related to git/GitHub common across scripts"""

from __future__ import annotations

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from functools import total_ordering
import re

# For type annotation simplification other modules may import Repo and Submodule from this module
from git.repo.base import Repo
from git.objects.submodule.base import Submodule
import github

GENAPSYS_GITHUB = "GenapsysInc"

APPROVED = "APPROVED"
COMMENTED = "COMMENTED"
CHANGES_REQUESTED = "CHANGES_REQUESTED"

RELEASE_VERSION_DELIM = "-"
SEMANTIC_VERSION_DELIM = "."
VERSION_TAG_REGEX = re.compile(rf"\d+{SEMANTIC_VERSION_DELIM}\d+{SEMANTIC_VERSION_DELIM}\d+{RELEASE_VERSION_DELIM}\d+")

REPO_SETTINGS = {"has_issues": "has_issues", "allow_rebase_merge": "allow_rebase_merge",
                 "delete_branch_on_merge": "delete_branch_on_merge", "has_wiki": "has_wiki",
                 "has_projects": "has_projects", "allow_squash_merge": "allow_squash_merge",
                 "allow_merge_commit": "allow_merge_commit", "allow_auto_merge": "allow_auto_merge"}

BRANCH_PROTECTION = {"require_code_owner_reviews": "require_code_owner_reviews",
                     "dismiss_stale_reviews": "dismiss_stale_reviews",
                     "required_conversation_resolution": "required_conversation_resolution",
                     "required_approving_review_count": "required_approving_review_count",
                     "enforce_admins": "enforce_admins",
                     "required_pull_request_reviews": "required_pull_request_reviews",
                     "restrictions": "restrictions",
                     "require_branches_uptodate": "strict", "required_passing_checks": "contexts",
                     "required_status_checks": "required_status_checks"}


class ConfigurationError(Exception):
    """Should be raised when input arguments are found to be incorrect/invalid"""


class InvalidVersion(Exception):
    """Should be raised when parsing a tag that does not conform to expected version format"""


@total_ordering
class VersionTag:
    """Representation of a git tag in the form of major.minor.patch-release"""

    def __init__(self, tag: str) -> None:
        """Ctor.

        :param tag: Tag string in "major.minor.patch-release" format
        """
        # Will be set by setting self.tag
        self.__major: int
        self.__minor: int
        self.__patch: int
        self.__release: int

        self.tag = tag

    def __str__(self) -> str:
        return self.tag

    def __eq__(self, other) -> bool:
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __lt__(self, other) -> bool:
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
    def tag(self, new_tag: str) -> None:
        """Assert valid format, store the given tag, and determine major, minor, patch, and release numbers

        :param new_tag: The new tag to store and parse
        """
        if match := re.match(VERSION_TAG_REGEX, new_tag):
            self.__tag = match.group()
        else:
            raise InvalidVersion(f"{new_tag} did not conform to major.minor.patch-release format")

        major_minor_patch, release = self.tag.split(RELEASE_VERSION_DELIM)
        major, minor, patch = major_minor_patch.split(SEMANTIC_VERSION_DELIM)

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

    def assert_valid_new_version(self, other: VersionTag) -> None:
        """Is the other VersionTag a valid increment of self? Asserts that the new version is >= the old version, that
        the minor and patch versions are 0 for a major increment, that the patch version is 0 for a minor increment, and
        that version increments are equal to 1.

        :param other: The VersionTag representing a version increment
        :raises InvalidVersion: If the given VersionTag is not a valid increment
        """
        # Current version is greater than the new one
        if self > other:
            raise InvalidVersion(f"Current version {self} > new version {other}")

        # Major version increment
        if other.major > self.major:
            if other.major - self.major != 1:
                raise InvalidVersion(f"Major version increment > 1 between {self} and {other}")
            if other.minor:
                raise InvalidVersion(f"Expected minor version of 0 with major version increment but was {other.minor}")
            if other.patch:
                raise InvalidVersion(f"Expected patch version of 0 with major version increment but was {other.patch}")

        # Minor version increment
        if other.minor > self.minor:
            if other.minor - self.minor != 1:
                raise InvalidVersion(f"Minor version increment > 1 between {self} and {other}")
            if other.patch:
                raise InvalidVersion(f"Expected patch version of 0 with minor version increment but was {other.patch}")

        # Patch version increment
        if other.patch > self.patch and other.patch - self.patch != 1:
            raise InvalidVersion(f"Patch version increment > 1 between {self} and {other}")

    def get_new_release(self) -> str:
        """Return a new tag with the release number incremented by 1

        :return: The new tag string
        """
        return (
            f"{self.major}{SEMANTIC_VERSION_DELIM}{self.minor}{SEMANTIC_VERSION_DELIM}"
            f"{self.patch}{RELEASE_VERSION_DELIM}{self.release + 1}"
        )


def get_repo_name_from_url(url: str) -> str:
    """Given a https/git url, get the repository name

    :param url: The url to parse, either https://github.com/... or git@github.com:...
    :return: The repository name parsed from the url
    """
    return url.split(".git")[0].split("/")[-1]


def get_repo_name(git_repo: Repo) -> str:
    """Given a GitPython Repo object, determine the name of the repository based on the remote

    :param git_repo: The Repo instance
    :return: The name of the repository
    """
    return get_repo_name_from_url(git_repo.remotes.origin.url)


def get_submodule_name(git_submodule: Submodule) -> str:
    """Given a GitPython Submodule object, determine the name of the submodule based on the remote

    :param git_submodule: The Submodule instance
    :return: The name of the repository
    """
    return get_repo_name_from_url(git_submodule.url)


def get_organization(client, org_name):
    """Wraps call to GitHub's Organization REST endpoint in a try/except"""
    try:
        return client.get_organization(org_name)
    except github.GithubException as exc:
        raise ConfigurationError(f"Could not retrieve organization {org_name} with given secret") from exc


def get_repo(org, repo_name):
    """Wraps call to GitHub's Repository REST endpoint in a try/except"""
    try:
        return org.get_repo(repo_name)
    except github.GithubException as exc:
        raise ConfigurationError(f"Could not find repo {repo_name} in organization {org.name}") from exc


def get_pull(repo, pull_number):
    """Wraps call to GitHub's Pulls REST endpoint in a try/except"""
    try:
        return repo.get_pull(pull_number)
    except github.GithubException as exc:
        raise ConfigurationError(f"Could not find PR in repo {repo.name} with number {pull_number}") from exc
