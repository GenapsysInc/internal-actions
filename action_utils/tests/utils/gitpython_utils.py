"""Utilities for testing GitPython usage, mocking of a lot of GitPyhon classes"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from unittest import mock


class MockIterableList(mock.Mock):
    def __init__(self, items):
        super().__init__()

        self.items = items

    def __getitem__(self, item):
        return self.items[item]

    def __getattr__(self, attr):
        for item in self.items:
            if hasattr(item, attr):
                return item

        return super().__getattr__(attr)


class MockGitSubmodule(mock.Mock):
    def __init__(self, url, commit):
        super().__init__()

        self.url = url
        self.commit = commit

    @property
    def hexsha(self):
        return self.commit


class MockGitRemote(mock.Mock):
    def __init__(self, name, url):
        super().__init__()

        self.name = name
        self.url = url

        setattr(self, name, self)


class MockGitRepo(mock.Mock):
    def __init__(self, remotes, submodules=None):
        super().__init__()

        self.remotes = MockIterableList(remotes)
        self.submodules = submodules if submodules else []

    def iter_submodules(self):
        return iter(self.submodules)
