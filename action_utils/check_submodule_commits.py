"""Asserts all submodules in a repository are on a commit in the default branch's commit history for that submodule"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import argparse
import sys

import git
import github

from action_utils import common


def submodule_is_valid(git_submodule: common.Submodule, github_repo: github.Repository.Repository) -> bool:
    """Determines if the given submodule is valid by looking through the git history for the default
    branch of the submodule

    :param submodule: The git submodule to inspect
    :param client: The GitHub Organization to use to pull commit history for the submodule
    :return: True if the submodule's commit is in the history of the default branch for the submodule, else False
    """
    if any(commit.sha == git_submodule.hexsha for commit in github_repo.get_commits(sha=github_repo.default_branch)):
        print(f"Found matching commit in {github_repo.name} in default branch {github_repo.default_branch}")
        return True

    print(f"Did NOT find matching commit in {github_repo.name} in default branch {github_repo.default_branch}")
    return False


def repo_has_valid_submodules(org_str: str, git_repo: common.Repo, github_client: github.MainClass.Github) -> bool:
    """Run validation check on each of the given Repo's submodules

    :param org_str: The GitHub organization to inspect
    :param repo: The Repo to inspect
    :param client: Authenticated Github client
    :return: True if all submodules passed the check, else False
    """
    try:
        org = github_client.get_organization(org_str)
    except github.GithubException as failed_org_query:
        raise common.ConfigurationError("Could not authenticate with given secret") from failed_org_query

    all_submodules_valid = True

    # Do this instead of an "all" so that each team's result is processed and output to stdout
    for git_submodule in git_repo.iter_submodules():
        github_repo = org.get_repo(common.get_submodule_name(git_submodule))
        all_submodules_valid &= submodule_is_valid(git_submodule, github_repo)

    repo_name = common.get_repo_name(git_repo)

    if not git_repo.submodules:
        print(f"Repository {repo_name} does not have any submodules, passing check by default")
    elif all_submodules_valid:
        print(f"All submodules in repository {repo_name} passed check")
    else:
        print(f"Not all submodules in repository {repo_name} passed check")

    return all_submodules_valid


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Assert a repo's submodules are on valid commits")

    parser.add_argument("-s", "--secret", required=True, help="GitHub token for authentication")

    parser.add_argument("-o", "--org", required=True, help="The GitHub organization to inspect")

    parser.add_argument("-r", "--repo-path", required=True, help="Local path to the repository to inspect")

    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_args()

    if repo_has_valid_submodules(opts.org, git.Repo(opts.repo_path), github.Github(opts.secret)):
        sys.exit(0)

    sys.exit(1)
