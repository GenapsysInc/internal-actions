"""Tag the current git commit based on version information in a JSON file"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import argparse
import datetime
import json

import git
import github

from action_utils import common


def tag_current_commit(git_repo: git.repo.base.Repo, new_version: str, add_date: bool = False) -> None:
    """Given a new version, tag the current commit accordingly

    :param new_version: The new version to use to tag
    :param add_date: Append current date to the tag
    :raises common.InvalidVersion: If the new version does not make sense with respect to the current version
    """
    old_version = git.


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Determine if relevant teams have approved a PR")

    parser.add_argument("-s", "--secret", required=True, help="GitHub token for authentication")

    parser.add_argument("-r", "--repo-path", required=True, help="Path to local git repository")

    parser.add_argument("-j", "--json", required=True, help="JSON file path")

    parser.add_argument("-d", "--date", action="store_true", required=False, help="Add a date string to the tag")

    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_args()

    with open(opts.json, 'r', encoding="utf-8") as json_fh:
        json_content = json.load(json_fh)

    tag_current_commit(git.Repo(opts.repo_path), json_content["version"], opts.date)
