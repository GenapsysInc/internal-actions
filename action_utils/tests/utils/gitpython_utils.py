"""Utilities for testing GitPython usage, mocking of a lot of GitPyhon classes"""
# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

from typing import Iterable, Any
from unittest import mock

import git


class MockIterableList(mock.Mock):
    """Mock of GitPython's IterableList class"""

    def __init__(self, items: list[Any]) -> None:
        super().__init__()

        self.items = items

    def __getitem__(self, item: int) -> Any:
        return self.items[item]

    def __getattr__(self, attr: str) -> Any:
        for item in self.items:
            if hasattr(item, attr):
                return item

        return super().__getattr__(attr)


class MockGitSubmodule(mock.Mock):
    """Mock of GitPython's Submodule class"""

    def __init__(self, url: str, commit: str) -> None:
        super().__init__()

        self.url = url
        self.commit = commit

    @property
    def hexsha(self) -> str:
        return self.commit


class MockGitRemote(mock.Mock):
    """Mock of GitPython's Remote class"""

    def __init__(self, name: str, url: str) -> None:
        super().__init__()

        self.name = name
        self.url = url

        setattr(self, name, self)


class MockGitTag(mock.Mock):
    """Mock of GitPython's Tag class"""

    def __init__(self, tag: str, message: str) -> None:
        super().__init__()

        self.tag = tag
        self.message = message


class GitErrorRaiser:
    """Object that will raise a GitError when called"""

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __call__(self, *args, **kwargs):
        raise git.GitError(self.msg)


class MockGitRepo(mock.Mock):
    """Mock of GitPython's Repo class"""

    def __init__(self, remotes: list[MockGitRemote], submodules: list[MockGitSubmodule] = None,
                 tags: list[MockGitTag] = None, latest_tag: MockGitTag = None):
        super().__init__()

        self.remotes = MockIterableList(remotes)
        self.submodules = submodules if submodules else []
        self.tags = tags if tags else []
        self.latest_tag = latest_tag
        self.git = mock.Mock()

        if latest_tag:
            self.git.describe = mock.Mock(return_value=self.latest_tag.tag)
        else:
            self.git.describe = GitErrorRaiser("No tags exist")

    def iter_submodules(self) -> Iterable[MockGitSubmodule]:
        return iter(self.submodules)

    def create_tag(self, tag_str: str, m: str = None) -> MockGitTag:  # pylint: disable=invalid-name
        if tag_str in [tag.tag for tag in self.tags]:
            raise git.GitError(f"Tag {tag_str} already exists")

        new_tag = MockGitTag(tag_str, message=m)

        self.tags.append(new_tag)
        self.latest_tag = new_tag

        return new_tag
