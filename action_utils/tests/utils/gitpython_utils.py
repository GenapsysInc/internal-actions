"""Utilities for testing GitPython usage, mocking of a lot of GitPyhon classes"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from unittest import mock

import git


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


class MockGitTag(mock.Mock):
    def __init__(self, tag, message):
        super().__init__()

        self.tag = tag
        self.message = message


class MockGitRepo(mock.Mock):
    def __init__(self, remotes, submodules=None, tags=None, latest_tag=None):
        super().__init__()

        self.remotes = MockIterableList(remotes)
        self.submodules = submodules if submodules else []
        self.tags = tags if tags else []
        self.latest_tag = latest_tag
        self.git = mock.Mock()

        if latest_tag:
            self.git.describe = mock.Mock(return_value=self.latest_tag.tag)

    def iter_submodules(self):
        return iter(self.submodules)

    def create_tag(self, tag_str, m=None):
        if tag_str in [tag.tag for tag in self.tags]:
            raise git.exc.GitCommandError(f"Tag {tag_str} already exists")

        new_tag = MockGitTag(tag_str, message=m)

        self.tags.append(new_tag)
        self.latest_tag = new_tag

        return new_tag
