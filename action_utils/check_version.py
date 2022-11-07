"""Assert repo version was bumped if a git diff implies it should have been"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import argparse
from fnmatch import fnmatch
import json
from pathlib import Path
import sys

import github

from action_utils import common


def _match(file_name: str, to_match: str) -> bool:
    """Determine if a file name matches a given string. If to_match is a directory and the given file lives within the
    directory, will return True. Otherwise, returns the result of a call to fnmatch

    :param file_name: The name of the file for the check
    :param to_match: The directory/file/pattern to match
    :return: The result of the comparison
    """
    if Path(to_match).is_dir() and file_name.startswith(f"{to_match.rstrip('/')}/"):
        return True

    return fnmatch(file_name, to_match)



def file_is_relevant(file_name: str, includes: list[str] = None, excludes: list[str] = None) -> bool:
    """Helper method that determines if a given file name is relevant for the check

    :param file_name: The name of the file to check
    :param includes: List of paths/patterns to be checked
    :param excludes: List of paths/patterns to be excluded from the check, taking priority over includes
    """
    includes, excludes = includes if includes else [], excludes if excludes else []

    # If the file matches an exclude pattern, then we don't care about it
    if any(_match(file_name, exclude) for exclude in excludes):
        return False

    # No excludes matched, if it matches any of the includes then we care about it, otherwise we don't
    return any(_match(file_name, include) for include in includes)


def missing_version_bump(
        client: github.MainClass.Github,
        org_name: str,
        repo_name: str,
        pull_number: int,
        version: common.VersionTag,
        includes: list[str] = None,
        excludes: list[str] = None
    ) -> bool:
    """Determines if a pull request should have incurred a version bump, and if so asserts that the version was bumped

    :param client: Authenticated PyGithub client
    :param org_name: The GitHub organization name
    :param repo_name: The GitHub repo name
    :param pull_number: The number of the pull request to inspect
    :param version: Version parsed from repo data JSON file
    :param includes: List of paths/patterns that when changed should incur a version bump
    :param excludes: List of paths/patterns that do not matter for version bumping - takes priority over includes
    :return: True if a version bump is required but was not made, False otherwise
    """
    org = common.get_organization(client, org_name)
    repo = common.get_repo(org, repo_name)
    pull = common.get_pull(repo, pull_number)

    version_bump_required = False

    for file in pull.get_files():
        if file_is_relevant(file.filename, includes=includes, excludes=excludes):
            version_bump_required = True
            break

    # If there is a tag matching the given version and a version bump is required, then fail the check
    # Note that this does not check for decrementing the version... the end use case is only intended to be a reminder
    if version.tag in (tag.name for tag in repo.get_tags()) and version_bump_required:
        return True

    return False


def main():
    """Main entrypoint"""
    opts = parse_args()

    with open(opts.json, "r", encoding="utf-8") as json_fh:
        json_content = json.load(json_fh)

    json_version = common.VersionTag(f"{json_content['version']}-1")

    client = github.Github(opts.secret)

    if missing_version_bump(client, opts.organization, opts.repo, opts.pull_number,
                            json_version, opts.include, opts.exclude):
        print(f"Version {json_version.tag} needs to be incremented based on found changes")
        sys.exit(1)

    sys.exit(0)


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Assert version was bumped if given changes imply it should have been")

    parser.add_argument("-j", "--json", required=True, help="JSON file path")

    parser.add_argument("-s", "--secret", required=True, help="GitHub auth token")

    parser.add_argument("-p", "--pull-number", required=True, type=int, help="Pull request number")

    parser.add_argument("-r", "--repo", required=True, help="Name of repo the pull request lives in")

    parser.add_argument("-o", "--organization", default=common.GENAPSYS_GITHUB, help="Organization the repo lives in")

    parser.add_argument("-i", "--include", nargs="*", help="Paths/wildcards to include in diff check")

    parser.add_argument("-e", "--exclude", nargs="*", help="Paths/wildcards to exclude in diff check")

    return parser.parse_args()


if __name__ == "__main__":
    main()
