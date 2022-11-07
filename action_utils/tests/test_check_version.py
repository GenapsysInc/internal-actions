"""Tests for the action_utils.check_version module"""
# pylint: disable=missing-function-docstring

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import pytest

from action_utils import check_version
from action_utils import common
import action_utils.tests.utils.pygithub_utils as pygh_utils


class TestFileIsRelevant:
    """Tests for the file_is_relevant utility function"""

    def test_include_match_no_exclude_match(self, tmp_path):
        """Test that when the include list is matched and the exclude list is not, True is returned"""
        path = str(tmp_path)
        (tmp_path / "subdir").mkdir()

        assert check_version.file_is_relevant("file.py", includes=["*.py"], excludes=["*.json"])
        assert check_version.file_is_relevant("file.py", includes=["file.py"], excludes=["*.json"])
        assert check_version.file_is_relevant(f"{path}/file.py", includes=[path], excludes=["tests"])
        assert check_version.file_is_relevant(f"{path}/file.py", includes=[f"{path}/"], excludes=["tests"])
        assert check_version.file_is_relevant(f"{path}/subdir/file.py", includes=[f"{path}/subdir"], excludes=["tests"])
        assert check_version.file_is_relevant("dir/file.py", includes=["*.py"], excludes=["*.json"])
        assert check_version.file_is_relevant("dir/subdir/file.py", includes=["dir/*/*.py"], excludes=["*.json"])

    def test_include_match_exclude_match(self, tmp_path):
        """Test that when the include list is matched but the exclude list is also matched, False is returned"""
        path = str(tmp_path)
        (tmp_path / "subdir").mkdir()

        assert not check_version.file_is_relevant("file.py", includes=["*.py"], excludes=["*.py"])
        assert not check_version.file_is_relevant("file.py", includes=["file.py"], excludes=["*.py"])
        assert not check_version.file_is_relevant("file.py", includes=["*.py"], excludes=["file.py"])
        assert not check_version.file_is_relevant(f"{path}/file.py", includes=["docs"], excludes=[path])
        assert not check_version.file_is_relevant("dir/file.py", includes=["*.py"], excludes=["*.py"])
        assert not check_version.file_is_relevant("dir/subdir/file.py", includes=["dir/*/*.py"], excludes=["*.py"])

    def test_no_include_match(self):
        """Test that when the include list is not matched, False is returned"""
        assert not check_version.file_is_relevant("file.py", includes=["*.json"], excludes=["*.yml"])
        assert not check_version.file_is_relevant("docs/file.py", includes=["*.json"], excludes=["*.yml"])
        assert not check_version.file_is_relevant("docs/sub/file.py", includes=["docs/no/*.py"], excludes=["*.yml"])

    def test_no_includes(self):
        """Test handling of empty include list"""
        assert not check_version.file_is_relevant("file.py", excludes=["*.yml"])

    def test_no_excludes(self):
        """Test handling of empty exclude list"""
        assert check_version.file_is_relevant("file.py", includes=["*.py"])


@pytest.fixture(name="gh_client")
def fixture_gh_client(gh_org):
    return pygh_utils.MockGithubClient({gh_org.name: gh_org})


@pytest.fixture(name="gh_org")
def fixture_gh_org(gh_repo):
    return pygh_utils.MockGithubOrg("my_org", repos={gh_repo.name: gh_repo})


@pytest.fixture(name="gh_repo")
def fixture_gh_repo(gh_pull, gh_tags):
    return pygh_utils.MockGithubRepo("my_repo", pulls={gh_pull.num: gh_pull}, tags=gh_tags)


@pytest.fixture(name="gh_tags")
def fixture_gh_tags():
    return [
        pygh_utils.MockGithubTag("1.0.0-1", pygh_utils.MockGithubCommit("")),
        pygh_utils.MockGithubTag("1.0.0-2", pygh_utils.MockGithubCommit("")),
        pygh_utils.MockGithubTag("1.1.0-1", pygh_utils.MockGithubCommit(""))
    ]


@pytest.fixture(name="gh_pull")
def fixture_gh_pull(gh_files):
    return pygh_utils.MockGithubPull(3, files=gh_files)


@pytest.fixture(name="gh_files")
def fixture_fh_files():
    return [
        pygh_utils.MockGithubFile("file.py", ""),
        pygh_utils.MockGithubFile("src/entrypoint.py", ""),
        pygh_utils.MockGithubFile("docs/conf.py", ""),
        pygh_utils.MockGithubFile("docs/subdir/file.py", "")
    ]


class TestMissingVersionBump:
    """Tests for the missing_version_bump function"""

    def test_no_relevant_files_changed(self, gh_client, gh_org, gh_repo, gh_pull):
        """Test that when no relevant files were changed, the check returns False"""
        version = common.VersionTag("1.0.0-1")
        includes = ["*.yml", "*.json"]
        excludes = []

        assert not check_version.missing_version_bump(gh_client, gh_org.name, gh_repo.name, gh_pull.num,
                                                      version, includes, excludes)

    def test_relevant_files_changed_version_bump(self, gh_client, gh_org, gh_repo, gh_pull):
        """Test that when relevant files were changed, and the version was bumped, the check returns False"""
        version = common.VersionTag("1.1.1-1")
        includes = ["*.py"]
        excludes = ["docs"]

        assert not check_version.missing_version_bump(gh_client, gh_org.name, gh_repo.name, gh_pull.num,
                                                      version, includes, excludes)

    def test_relevant_files_changed_no_version_bump(self, gh_client, gh_org, gh_repo, gh_pull):
        """Test that when relevant files were changed, and the version was not bumped, the check returns True"""
        version = common.VersionTag("1.1.0-1")
        includes = ["*.py"]
        excludes = ["docs"]

        assert check_version.missing_version_bump(gh_client, gh_org.name, gh_repo.name, gh_pull.num,
                                                  version, includes, excludes)
