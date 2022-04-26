"""Utilities for testing PyGithub usage, mocking of a lot of PyGithub classes"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from unittest import mock

import github


class MockGithubException(github.GithubException):
    def __init__(self, msg):
        super().__init__(None, None, None)

        self.msg = msg

    def __str__(self):
        return self.msg


class MockGithubUser(mock.Mock):
    def __init__(self, name):
        super().__init__()

        self.name = name

    def __hash__(self):
        return hash(self.name)


class MockGithubTeam(mock.Mock):
    def __init__(self, name, users):
        super().__init__()

        self.name = name
        self.users = users

    def get_members(self):
        return self.users


class MockGithubReview(mock.Mock):
    def __init__(self, user, state):
        super().__init__()

        self.user = user
        self.state = state


class MockGithubPull(mock.Mock):
    def __init__(self, pull_num, reviews):
        super().__init__()

        self.num = pull_num
        self.reviews = reviews

    def get_reviews(self):
        return self.reviews


class MockGithubRepo(mock.Mock):
    def __init__(self, name, pulls=None):
        super().__init__()

        self.name = name
        self.pulls = pulls if pulls else {}

    def add_pull(self, pull):
        self.pulls[pull.num] = pull

    def get_pull(self, pull_num):
        if pull_num not in self.pulls:
            raise MockGithubException(f"Couldn't find pull request {pull_num}")

        return self.pulls[pull_num]


class MockGithubOrg(mock.Mock):
    def __init__(self, name, teams=None, repos=None):
        super().__init__()

        self.name = name
        self.teams = teams if teams else {}
        self.repos = repos if repos else {}

    def add_repo(self, repo):
        self.repos[repo.name] = repo

    def get_repo(self, repo_name):
        if repo_name not in self.repos:
            raise MockGithubException(f"Couldn't find repo {repo_name}")

        return self.repos[repo_name]

    def get_repos(self):
        return self.repos.values()

    def add_team(self, team):
        self.teams[team.name] = team

    def get_team(self, team_name):
        if team_name not in self.teams:
            raise MockGithubException(f"Couldn't find team {team_name}")

        return self.teams[team_name]

    def get_teams(self):
        return self.teams.values()


class MockGithubClient(mock.Mock):
    def __init__(self, orgs, authenticated=True):
        super().__init__()

        self.orgs = orgs if orgs else {}
        self.authenticated = authenticated

    def get_organization(self, org):
        if not self.authenticated:
            raise MockGithubException("Authentication failed")

        return self.orgs[org]
