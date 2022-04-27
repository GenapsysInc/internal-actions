"""Unit tests for the action_utils.check_submodule_commits module"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import pytest

from action_utils import common
import action_utils.check_submodule_commits as csc
import action_utils.tests.utils.gitpython_utils as gpy_utils


@pytest.fixture(name="git_submodule_1")
def fixture_git_submodule_1():
    return gpy_utils.MockGitSubmodule("git@github.com:test_org/submod_1", "c6ab5c34293c5d4c4b845ff1fb43b6c1a14efc0f")


@pytest.fixture(name="git_submodule_2")
def fixture_git_submodule_2():
    return gpy_utils.MockGitSubmodule("git@github.com:test_org/submod_2", "605ec24162595201e00bf749142049049e886b38")


@pytest.fixture(name="git_submodule_3")
def fixture_git_submodule_3():
    return gpy_utils.MockGitSubmodule("git@github.com:test_org/submod_3", "cc1094a52793eef40bf7fcc55186d7d25a91057f")


@pytest.fixture(name="git_submodule_4")
def fixture_git_submodule_4():
    return gpy_utils.MockGitSubmodule("git@github.com:test_org/submod_4", "5ed147fe12ec412b484c8ec7fd44bf550e454b13")


@pytest.fixture(name="git_remote")
def fixture_git_remote():
    return gpy_utils.MockGitRemote("origin", "git@github.com:test_org/test_repo")


@pytest.fixture(name="git_repo")
def fixture_git_repo(git_remote, git_submodule_1, git_submodule_2):
    return gpy_utils.MockGitRepo([git_remote], submodules=[git_submodule_1, git_submodule_2])


@pytest.fixture(name="github_commits_1")
def fixture_github_commits_1():
    pass


@pytest.fixture(name="github_commits_2")
def fixture_github_commits_2():
    pass


@pytest.fixture(name="github_submodule_1")
def fixture_github_submodule_1():
    pass


@pytest.fixture(name="github_submodule_2")
def fixture_github_submodule_2():
    pass


@pytest.fixture(name="github_submodule_3")
def fixture_github_submodule_3():
    pass


@pytest.fixture(name="github_submodule_4")
def fixture_github_submodule_4():
    pass


@pytest.fixture(name="github_repo_all_valid")
def fixture_github_repo_all_valid():
    pass


@pytest.fixture(name="github_repo_all_invalid")
def fixture_github_repo_all_invalid():
    pass


@pytest.fixture(name="github_repo_mixed")
def fixture_github_repo_mixed():
    pass
