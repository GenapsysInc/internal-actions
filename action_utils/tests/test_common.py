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


def test_get_repo_name_from_url_git(git_url):
    """Assert correct parsing of a git url"""
    assert common.get_repo_name_from_url(git_url) == TEST_GIT_REPO


def test_get_repo_name_from_url_https(https_url):
    """Assert correct parsing of a https url"""
    assert common.get_repo_name_from_url(https_url) == TEST_HTTPS_REPO


def test_get_repo_name(repo):
    """Test getting repository name from Repo object"""
    assert common.get_repo_name(repo) == TEST_GIT_REPO


def test_get_submodule_name(submodule):
    """Test getting repository name from Submodule object"""
    assert common.get_submodule_name(submodule) == TEST_GIT_REPO
