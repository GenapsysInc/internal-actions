"""Tests for the action_utils.tag_commit module"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from datetime import date
import pytest

from action_utils import common, tag_commit
import action_utils.tests.utils.gitpython_utils as gpy_utils


@pytest.fixture(name="git_remote")
def fixture_git_remote():
    return gpy_utils.MockGitRemote("origin", "git@github.com:my_org/my_repo")


@pytest.fixture(name="git_tag")
def fixture_git_tag():
    return gpy_utils.MockGitTag("1.2.3-4-1-ac76a63e", message="1.2.3-4-1-ac76a63e")


@pytest.fixture(name="git_repo")
def fixture_git_repo(git_remote, git_tag):
    return gpy_utils.MockGitRepo([git_remote], tags=[git_tag], latest_tag=git_tag)


class TestTagCurrentCommit:
    """Tests for the tag_current_commit function"""

    @staticmethod
    def test_major_bump(git_repo):
        """Test successful major version bump when given valid new version"""
        new_version = common.VersionTag("2.0.0-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "2.0.0-1"
        assert git_repo.latest_tag.message == "2.0.0-1"

    @staticmethod
    def test_minor_bump(git_repo):
        """Test successful minor version bump when given valid new version"""
        new_version = common.VersionTag("1.3.0-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.3.0-1"
        assert git_repo.latest_tag.message == "1.3.0-1"

    @staticmethod
    def test_patch_bump(git_repo):
        """Test successful patch version bump when given valid new version"""
        new_version = common.VersionTag("1.2.4-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.2.4-1"
        assert git_repo.latest_tag.message == "1.2.4-1"

    @staticmethod
    def test_release_bump(git_repo):
        """Test successful release version bump when given valid new version"""
        new_version = common.VersionTag("1.2.3-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.2.3-5"
        assert git_repo.latest_tag.message == "1.2.3-5"

    @staticmethod
    def test_bump_with_date(git_repo):
        """Test successful version bump when requested to add current date"""
        new_version = common.VersionTag("2.0.0-1")
        tag_commit.tag_current_commit(git_repo, new_version, add_date=True)

        assert git_repo.latest_tag.tag == f"2.0.0-1-{date.today().strftime('%Y-%m-%d')}"
        assert git_repo.latest_tag.message == f"2.0.0-1-{date.today().strftime('%Y-%m-%d')}"

    @staticmethod
    def test_invalid_bump(git_repo):
        """Test handling of invalid version bump - exhaustive cases are handled in tests for common.VersionTag"""
        new_version = common.VersionTag("3.0.0-1")

        with pytest.raises(common.InvalidVersion):
            tag_commit.tag_current_commit(git_repo, new_version)
