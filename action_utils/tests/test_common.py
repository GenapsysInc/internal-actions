"""Unit tests for the action_utils.common module"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import pytest

from action_utils import common
import action_utils.tests.utils.gitpython_utils as gpy_utils

TEST_GIT_REPO = "test_git_repo"
TEST_HTTPS_REPO = "test_https_repo"


@pytest.fixture(name="git_url")
def fixture_git_url():
    return f"git@github.com:some_org/{TEST_GIT_REPO}"


@pytest.fixture(name="https_url")
def fixture_https_url():
    return f"https://github.com/some_org/{TEST_HTTPS_REPO}"


@pytest.fixture(name="remote")
def fixture_origin_remote(git_url):
    return gpy_utils.MockGitRemote("origin", git_url)


@pytest.fixture(name="repo")
def fixture_repo(remote):
    return gpy_utils.MockGitRepo([remote])


@pytest.fixture(name="submodule")
def fixture_submodule(git_url):
    return gpy_utils.MockGitSubmodule(git_url, "c6ab5c34293c5d4c4b845ff1fb43b6c1a14efc0f")


@pytest.fixture(name="patch_1")
def fixture_patch_1():
    return common.VersionTag("0.0.1-1")


@pytest.fixture(name="patch_2")
def fixture_patch_2():
    return common.VersionTag("0.0.2-1")


@pytest.fixture(name="minor_1")
def fixture_minor_1():
    return common.VersionTag("0.1.0-1")


@pytest.fixture(name="minor_2")
def fixture_minor_2():
    return common.VersionTag("0.2.0-1")


@pytest.fixture(name="major_1")
def fixture_major_1():
    return common.VersionTag("1.0.0-1")


@pytest.fixture(name="major_2")
def fixture_major_2():
    return common.VersionTag("2.0.0-1")


@pytest.fixture(name="major_with_new_release")
def fixture_major_with_new_release():
    return common.VersionTag("2.0.0-2")


@pytest.fixture(name="version_with_date")
def fixture_version_with_date():
    return common.VersionTag("2.0.0-2-05022022")


@pytest.fixture(name="version_with_commit")
def fixture_version_with_commit():
    return common.VersionTag("2.0.0-2-1-ac5601de")


@pytest.fixture(name="version_with_date_and_commit")
def fixture_version_with_date_and_commit():
    return common.VersionTag("2.0.0-2-05022022-1-ac5601de")


class TestGetRepoNameFromUrl:
    """Tests for the get_repo_name_from_url function"""

    @staticmethod
    def test_from_git_url(git_url):
        """Assert correct parsing of a git url"""
        assert common.get_repo_name_from_url(git_url) == TEST_GIT_REPO

    @staticmethod
    def test_from_https_url(https_url):
        """Assert correct parsing of a https url"""
        assert common.get_repo_name_from_url(https_url) == TEST_HTTPS_REPO


class TestGetRepoName:
    """Tests for the get_repo_name function"""

    @staticmethod
    def test_get_repo_name(repo):
        """Test getting repository name from Repo object"""
        assert common.get_repo_name(repo) == TEST_GIT_REPO


class TestGetSubmoduleName:
    """Tests for the get_submodule_name function"""

    @staticmethod
    def test_get_submodule_name(submodule):
        """Test getting repository name from Submodule object"""
        assert common.get_submodule_name(submodule) == TEST_GIT_REPO


class TestVersionTag:
    """Tests for the VersionTag class"""

    @staticmethod
    def test_major_minor_patch_release_standard(major_with_new_release):
        assert major_with_new_release.major == 2
        assert major_with_new_release.minor == 0
        assert major_with_new_release.patch == 0
        assert major_with_new_release.release == 2

    @staticmethod
    def test_major_minor_patch_release_date_added(version_with_date):
        assert version_with_date.major == 2
        assert version_with_date.minor == 0
        assert version_with_date.patch == 0
        assert version_with_date.release == 2

    @staticmethod
    def test_major_minor_patch_release_commit_addded(version_with_commit):
        assert version_with_commit.major == 2
        assert version_with_commit.minor == 0
        assert version_with_commit.patch == 0
        assert version_with_commit.release == 2

    @staticmethod
    def test_major_minor_patch_release_date_and_commit_added(version_with_date_and_commit):
        assert version_with_date_and_commit.major == 2
        assert version_with_date_and_commit.minor == 0
        assert version_with_date_and_commit.patch == 0
        assert version_with_date_and_commit.release == 2

    @staticmethod
    def test_invalid_tag_handling():
        with pytest.raises(common.InvalidVersion):
            common.VersionTag("not remotely a version")

        with pytest.raises(common.InvalidVersion):
            common.VersionTag("a.2.3-4")

        with pytest.raises(common.InvalidVersion):
            common.VersionTag("1.b.3-4")

        with pytest.raises(common.InvalidVersion):
            common.VersionTag("1.2.c-4")

        with pytest.raises(common.InvalidVersion):
            common.VersionTag("1.2.3-d")

    @staticmethod
    def test_get_new_release(major_with_new_release):
        assert major_with_new_release.get_new_release() == "2.0.0-3"

    @staticmethod
    def test_str(major_1):
        assert str(major_1) == "1.0.0-1"

    @staticmethod
    def test_operator_major_major(major_1, major_2):
        assert major_1 < major_2
        assert major_1 <= major_2
        assert major_2 > major_1
        assert major_2 >= major_1
        assert major_1 == major_1
        assert major_2 == major_2
        assert major_1 != major_2
        assert not major_1 < major_1
        assert not major_2 < major_2

    @staticmethod
    def test_operator_major_minor(major_1, minor_1):
        assert minor_1 < major_1
        assert minor_1 <= major_1
        assert major_1 > minor_1
        assert major_1 >= minor_1
        assert major_1 != minor_1

    @staticmethod
    def test_operator_major_patch(major_1, patch_1):
        assert patch_1 < major_1
        assert patch_1 <= major_1
        assert major_1 > patch_1
        assert major_1 >= patch_1
        assert major_1 != patch_1

    @staticmethod
    def test_operator_minor_minor(minor_1, minor_2):
        assert minor_1 < minor_2
        assert minor_1 <= minor_2
        assert minor_2 > minor_1
        assert minor_2 >= minor_1
        assert minor_1 == minor_1
        assert minor_2 == minor_2
        assert minor_1 != minor_2
        assert not minor_1 < minor_1
        assert not minor_2 < minor_2

    @staticmethod
    def test_operator_minor_patch(minor_1, patch_1):
        assert patch_1 < minor_1
        assert patch_1 <= minor_1
        assert minor_1 > patch_1
        assert minor_1 >= patch_1
        assert minor_1 != patch_1

    @staticmethod
    def test_operator_patch_patch(patch_1, patch_2):
        assert patch_1 < patch_2
        assert patch_1 <= patch_2
        assert patch_2 > patch_1
        assert patch_2 >= patch_1
        assert patch_1 == patch_1
        assert patch_2 == patch_2
        assert patch_1 != patch_2
        assert not patch_1 < patch_1
        assert not patch_2 < patch_2
