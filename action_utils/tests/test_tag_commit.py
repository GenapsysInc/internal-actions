"""Tests for the action_utils.tag_commit module"""
# pylint: disable=missing-function-docstring

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


@pytest.fixture(name="no_tag_repo")
def fixture_no_tag_repo(git_remote):
    return gpy_utils.MockGitRepo([git_remote])


class TestTagCurrentCommit:
    """Tests for the tag_current_commit function"""

    def test_major_bump(self, git_repo):
        """Test successful major version bump when given valid new version"""
        new_version = common.VersionTag("2.0.0-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "2.0.0-1"
        assert git_repo.latest_tag.message == "2.0.0-1"

    def test_minor_bump(self, git_repo):
        """Test successful minor version bump when given valid new version"""
        new_version = common.VersionTag("1.3.0-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.3.0-1"
        assert git_repo.latest_tag.message == "1.3.0-1"

    def test_patch_bump(self, git_repo):
        """Test successful patch version bump when given valid new version"""
        new_version = common.VersionTag("1.2.4-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.2.4-1"
        assert git_repo.latest_tag.message == "1.2.4-1"

    def test_release_bump(self, git_repo):
        """Test successful release version bump when given valid new version"""
        new_version = common.VersionTag("1.2.3-1")
        tag_commit.tag_current_commit(git_repo, new_version)

        assert git_repo.latest_tag.tag == "1.2.3-5"
        assert git_repo.latest_tag.message == "1.2.3-5"

    def test_bump_with_date(self, git_repo):
        """Test successful version bump when requested to add current date"""
        new_version = common.VersionTag("2.0.0-1")
        tag_commit.tag_current_commit(git_repo, new_version, add_date=True)

        assert git_repo.latest_tag.tag == f"2.0.0-1-{date.today().strftime('%Y-%m-%d')}"
        assert git_repo.latest_tag.message == f"2.0.0-1-{date.today().strftime('%Y-%m-%d')}"

    def test_no_current_tag_major(self, no_tag_repo):
        """Test successful major version bump when repo doesn't have any tags that exist"""
        new_version = common.VersionTag("1.0.0-1")
        tag_commit.tag_current_commit(no_tag_repo, new_version)

        assert no_tag_repo.latest_tag.tag == "1.0.0-1"
        assert no_tag_repo.latest_tag.message == "1.0.0-1"

    def test_no_current_tag_minor(self, no_tag_repo):
        """Test successful minor version bump when repo doesn't have any tags that exist"""
        new_version = common.VersionTag("0.1.0-1")
        tag_commit.tag_current_commit(no_tag_repo, new_version)

        assert no_tag_repo.latest_tag.tag == "0.1.0-1"
        assert no_tag_repo.latest_tag.message == "0.1.0-1"

    def test_no_current_tag_patch(self, no_tag_repo):
        """Test successful patch version bump when repo doesn't have any tags that exist"""
        new_version = common.VersionTag("0.0.1-1")
        tag_commit.tag_current_commit(no_tag_repo, new_version)

        assert no_tag_repo.latest_tag.tag == "0.0.1-1"
        assert no_tag_repo.latest_tag.message == "0.0.1-1"

    def test_no_current_tag_release(self, no_tag_repo):
        """Test successful laying down of 0.0.0-1 when repo doesn't have any tags that exist"""
        new_version = common.VersionTag("0.0.0-1")
        tag_commit.tag_current_commit(no_tag_repo, new_version)

        assert no_tag_repo.latest_tag.tag == "0.0.0-1"
        assert no_tag_repo.latest_tag.message == "0.0.0-1"

    def test_no_current_tag_bad_version(self, no_tag_repo):
        """Test that when a repo doesn't have any tags and a version > 1 is given, InvalidVersion is raised"""
        new_version = common.VersionTag("2.0.0-1")

        with pytest.raises(common.InvalidVersion):
            tag_commit.tag_current_commit(no_tag_repo, new_version)

    def test_invalid_bump(self, git_repo):
        """Test handling of invalid version bump - exhaustive cases are handled in tests for common.VersionTag"""
        new_version = common.VersionTag("3.0.0-1")

        with pytest.raises(common.InvalidVersion):
            tag_commit.tag_current_commit(git_repo, new_version)

    def test_duplicate_version(self, git_repo):
        """Test handling of error produced when trying to lay down a tag that already exists"""
        git_repo.create_tag("2.0.0-1", m="2.0.0-1")
        new_version = common.VersionTag("2.0.0-1")

        with pytest.raises(common.ConfigurationError):
            tag_commit.tag_current_commit(git_repo, new_version)
