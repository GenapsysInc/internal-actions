"""Unit tests for the action_utils.check_submodule_commits module"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import pytest

from action_utils import common
import action_utils.check_submodule_commits as csc
import action_utils.tests.utils.gitpython_utils as gpy_utils
import action_utils.tests.utils.pygithub_utils as pgh_utils

TEST_ORG = "test_org"
TEST_REPO = "test_repo"
SUBMOD_1 = "submod_1"
SUBMOD_2 = "submod_2"
SUBMOD_3 = "submod_3"
SUBMOD_4 = "submod_4"


@pytest.fixture(name="git_submodule_1")
def fixture_git_submodule_1():
    return gpy_utils.MockGitSubmodule(
        f"git@github.com:{TEST_ORG}/{SUBMOD_1}", "c6ab5c34293c5d4c4b845ff1fb43b6c1a14efc0f"
    )


@pytest.fixture(name="git_submodule_2")
def fixture_git_submodule_2():
    return gpy_utils.MockGitSubmodule(
        f"git@github.com:{TEST_ORG}/{SUBMOD_2}", "605ec24162595201e00bf749142049049e886b38"
    )


@pytest.fixture(name="git_submodule_3")
def fixture_git_submodule_3():
    return gpy_utils.MockGitSubmodule(
        f"git@github.com:{TEST_ORG}/{SUBMOD_3}", "cc1094a52793eef40bf7fcc55186d7d25a91057f"
    )


@pytest.fixture(name="git_submodule_4")
def fixture_git_submodule_4():
    return gpy_utils.MockGitSubmodule(
        f"git@github.com:{TEST_ORG}/{SUBMOD_4}", "5ed147fe12ec412b484c8ec7fd44bf550e454b13"
    )


@pytest.fixture(name="git_remote")
def fixture_git_remote():
    return gpy_utils.MockGitRemote("origin", f"git@github.com:{TEST_ORG}/{TEST_REPO}")


@pytest.fixture(name="git_repo_all_valid")
def fixture_git_repo_all_valid(git_remote, git_submodule_1, git_submodule_2):
    return gpy_utils.MockGitRepo([git_remote], submodules=[git_submodule_1, git_submodule_2])


@pytest.fixture(name="git_repo_all_invalid")
def fixture_git_repo_all_invalid(git_remote, git_submodule_3, git_submodule_4):
    return gpy_utils.MockGitRepo([git_remote], submodules=[git_submodule_3, git_submodule_4])


@pytest.fixture(name="git_repo_mixed")
def fixture_git_repo_mixed(git_remote, git_submodule_1, git_submodule_3):
    return gpy_utils.MockGitRepo([git_remote], submodules=[git_submodule_1, git_submodule_3])


@pytest.fixture(name="git_repo_no_submodules")
def fixture_git_repo_no_submodules(git_remote):
    return gpy_utils.MockGitRepo([git_remote])


@pytest.fixture(name="github_commits_1")
def fixture_github_commits_1():
    return {
        "main": [
            pgh_utils.MockGithubCommit("c6ab5c34293c5d4c4b845ff1fb43b6c1a14efc0f"),  # Matches submodule 1
            pgh_utils.MockGithubCommit("444dddee968683f7877b7d13a37ed3cf02c283a1"),
            pgh_utils.MockGithubCommit("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
            pgh_utils.MockGithubCommit("7c0112a0270b94686f0391b747b8f7057b4e5893"),
        ]
    }


@pytest.fixture(name="github_commits_2")
def fixture_github_commits_2():
    return {
        "main": [
            pgh_utils.MockGithubCommit("53b7e06122de22210291cde6e6fcd49c84e68676"),
            pgh_utils.MockGithubCommit("b8d97005fac09e74c4a0c51a5c64c5f0c077ffdb"),
            pgh_utils.MockGithubCommit("605ec24162595201e00bf749142049049e886b38"),  # Matches submodule 2
            pgh_utils.MockGithubCommit("c850af526faeabf304bbf316b1ae2a11bbcecd1d"),
        ]
    }


@pytest.fixture(name="github_submodule_1")
def fixture_github_submodule_1(github_commits_1):
    return pgh_utils.MockGithubRepo(SUBMOD_1, commits=github_commits_1)


@pytest.fixture(name="github_submodule_2")
def fixture_github_submodule_2(github_commits_2):
    return pgh_utils.MockGithubRepo(SUBMOD_2, commits=github_commits_2)


@pytest.fixture(name="github_submodule_3")
def fixture_github_submodule_3(github_commits_1):
    return pgh_utils.MockGithubRepo(SUBMOD_3, commits=github_commits_1)


@pytest.fixture(name="github_submodule_4")
def fixture_github_submodule_4(github_commits_2):
    return pgh_utils.MockGithubRepo(SUBMOD_4, commits=github_commits_2)


@pytest.fixture(name="github_org")
def fixture_github_org(github_submodule_1, github_submodule_2, github_submodule_3, github_submodule_4):
    org_repos = [github_submodule_1, github_submodule_2, github_submodule_3, github_submodule_4]
    repo_map = {repo.name: repo for repo in org_repos}
    return pgh_utils.MockGithubOrg(common.GENAPSYS_GITHUB, repos=repo_map)


@pytest.fixture(name="github_authed_client")
def fixture_github_authed_client(github_org):
    return pgh_utils.MockGithubClient({common.GENAPSYS_GITHUB: github_org}, authenticated=True)


@pytest.fixture(name="github_unauthed_client")
def fixture_github_unauthed_client(github_org):
    return pgh_utils.MockGithubClient({common.GENAPSYS_GITHUB: github_org}, authenticated=False)


class TestSubmoduleIsValid:
    """Tests for the submodule_is_valid function"""

    @staticmethod
    def test_valid(git_submodule_1, github_submodule_1):
        """Test submodule commit being in list of commits in github"""
        assert csc.submodule_is_valid(git_submodule_1, github_submodule_1)

    @staticmethod
    def test_invalid(git_submodule_3, github_submodule_3):
        """Test submodule commit not being in list of commits in github"""
        assert not csc.submodule_is_valid(git_submodule_3, github_submodule_3)


class TestRepoHasValidSubmodules:
    """Tests for the repo_has_valid_submodules function"""

    @staticmethod
    def test_all_valid(git_repo_all_valid, github_authed_client):
        """End-to-end style test, repo has 2 submodules on valid commits"""
        assert csc.repo_has_valid_submodules(git_repo_all_valid, github_authed_client)

    @staticmethod
    def test_mixed_valid(git_repo_mixed, github_authed_client):
        """End-to-end style test, repo has 1 submodule on a valid commit, but another on an invalid commit"""
        assert not csc.repo_has_valid_submodules(git_repo_mixed, github_authed_client)

    @staticmethod
    def test_none_valid(git_repo_all_invalid, github_authed_client):
        """End-to-end style test, repo has 2 submodules on invalid commits"""
        assert not csc.repo_has_valid_submodules(git_repo_all_invalid, github_authed_client)

    @staticmethod
    def test_no_submodules(git_repo_no_submodules, github_authed_client):
        """End-to-end style test, repo has no submodules so it should pass by default"""
        assert csc.repo_has_valid_submodules(git_repo_no_submodules, github_authed_client)

    @staticmethod
    def test_auth_failure(git_repo_all_valid, github_unauthed_client):
        """Assert proper handling of authentication failure"""
        with pytest.raises(common.ConfigurationError):
            csc.repo_has_valid_submodules(git_repo_all_valid, github_unauthed_client)
