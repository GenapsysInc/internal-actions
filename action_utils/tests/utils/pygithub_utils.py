"""Utilities for testing PyGithub usage, mocking of a lot of PyGithub classes"""
# pylint: disable=missing-function-docstring,missing-class-docstring

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from collections import defaultdict
from typing import DefaultDict, ValuesView
from unittest import mock

import github


class MockGithubException(github.GithubException):
    """Subclass of GithubException that acts like a "normal" Exception"""

    def __init__(self, msg: str) -> None:
        super().__init__(None, None, None)

        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class MockGithubUser(mock.Mock):
    """Mock of PyGithub's NamedUser class"""

    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def __hash__(self) -> int:
        return hash(self.name)


class MockGithubTeam(mock.Mock):
    """Mock of PyGithub's Team class"""

    def __init__(self, name: str, users: list[MockGithubUser]):
        super().__init__()

        self.name = name
        self.users = users

    def get_members(self) -> list[MockGithubUser]:
        return self.users


class MockGithubReview(mock.Mock):
    """Mock of PyGithub's PullRequestReview class"""

    def __init__(self, user: MockGithubUser, state: str) -> None:
        super().__init__()

        self.user = user
        self.state = state


class MockGithubCommit(mock.Mock):
    """Mock of PyGithub's Commit class"""

    def __init__(self, sha: str) -> None:
        super().__init__()

        self.sha = sha


class MockGithubTag(mock.Mock):
    """Mock of PyGithub's Tag class"""

    def __init__(self, name: str, commit: MockGithubCommit) -> None:
        super().__init__()

        self.name = name
        self.commit = commit


class MockGithubFile(mock.Mock):
    """Mock of PyGithub's File class"""

    def __init__(self, filename: str, sha: str) -> None:
        super().__init__()

        self.filename = filename
        self.sha = sha


class MockGithubPull(mock.Mock):
    """Mock of PyGithub's PullRequest class"""

    def __init__(self,
            pull_num: int,
            reviews: list[MockGithubReview] = None,
            files: list[MockGithubFile] = None
        ) -> None:
        super().__init__()

        self.num = pull_num
        self.reviews = reviews
        self.files = files

    def get_reviews(self) -> list[MockGithubReview]:
        return self.reviews

    def get_files(self) -> list[MockGithubFile]:
        return self.files


class MockGithubRepo(mock.Mock):
    """Mock of PyGithub's Repository class"""

    def __init__(
            self,
            name: str,
            default_branch: str = "main",
            commits: DefaultDict[str, list[MockGithubCommit]] = None,
            pulls: dict[int, MockGithubPull] = None,
            tags: list[MockGithubTag] = None
        ) -> None:
        super().__init__()

        self.name = name
        self.default_branch = default_branch
        self.commits = commits if commits else defaultdict(list)
        self.pulls = pulls if pulls else {}
        self.tags = tags if tags else []

    def add_commit(self, branch: str, commit: MockGithubCommit) -> None:
        self.commits[branch].append(commit)

    def get_commits(self, sha: str = None) -> list[MockGithubCommit]:
        return self.commits[sha]

    def add_pull(self, pull: MockGithubPull) -> None:
        self.pulls[pull.num] = pull

    def get_pull(self, pull_num: int) -> MockGithubPull:
        if pull_num not in self.pulls:
            raise MockGithubException(f"Couldn't find pull request {pull_num}")

        return self.pulls[pull_num]

    def get_tags(self) -> list[MockGithubTag]:
        return self.tags


class MockGithubOrg(mock.Mock):
    """Mock of PyGithub's Organization class"""

    def __init__(
            self,
            name: str,
            teams: dict[str, MockGithubTeam] = None,
            repos: dict[str, MockGithubRepo] = None
        ) -> None:
        super().__init__()

        self.name = name
        self.teams = teams if teams else {}
        self.repos = repos if repos else {}

    def add_repo(self, repo: MockGithubRepo) -> None:
        self.repos[repo.name] = repo

    def get_repo(self, repo_name: str) -> MockGithubRepo:
        if repo_name not in self.repos:
            raise MockGithubException(f"Couldn't find repo {repo_name}")

        return self.repos[repo_name]

    def get_repos(self) -> ValuesView[MockGithubRepo]:
        return self.repos.values()

    def add_team(self, team: MockGithubTeam) -> None:
        self.teams[team.name] = team

    def get_team(self, team_name: str) -> MockGithubTeam:
        if team_name not in self.teams:
            raise MockGithubException(f"Couldn't find team {team_name}")

        return self.teams[team_name]

    def get_teams(self) -> ValuesView[MockGithubTeam]:
        return self.teams.values()


class MockGithubClient(mock.Mock):
    """Mock of PyGithub's Github class"""

    def __init__(self, orgs: dict[str, MockGithubOrg], authenticated: bool = True):
        super().__init__()

        self.orgs = orgs if orgs else {}
        self.authenticated = authenticated

    def get_organization(self, org: str) -> MockGithubOrg:
        if not self.authenticated:
            raise MockGithubException("Authentication failed")

        return self.orgs[org]
