"""Assert repo version was bumped if a git diff implies it should have been"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import argparse
import json

import github

from action_utils import common

def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Assert version was bumped if given changes imply it should have been")

    parser.add_argument("-j", "--json", required=True, help="JSON file path")

    parser.add_argument("-s", "--secret", required=True, help="GitHub auth token")

    parser.add_argument("-p", "--pull-number", required=True, help="Pull request number")

    parser.add_argument("-r", "--repo", required=True, help="Name of repo the pull request lives in")

    parser.add_argument("-o", "--organization", default=common.GENAPSYS_GITHUB, help="Organization the repo lives in")

    parser.add_argument("-i", "--include", nargs="*", help="Paths/wildcards to include in diff check")

    parser.add_argument("-e", "--exclude", nargs="*", help="Paths/wildcards to exclude in diff check")

    return parser.parse_args()


def temp_name(client, org_name, repo_name, pr_num, version, include, exclude):
    org = common.get_organization(client, org_name)

    pull = common.get_pull(org, repo_name, pr_num)

    return pull


def main():
    opts = parse_args()

    with open(opts.json, "r", encoding="utf-8") as json_fh:
        json_content = json.load(json_fh)

    json_version = common.VersionTag(f"{json_content['version']}-1")

    client = github.Github(opts.secret)

    temp_name(client, opts.organization, opts.repo, opts.pull_number, json_version, opts.include, opts.exclude)


if __name__ == "__main__":
    main()
