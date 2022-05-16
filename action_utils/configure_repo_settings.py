"""Configure and check repository settings"""

__author__ = "Aaron Berlin"

import argparse
import sys

import github

from action_utils import common


org_repo_policy = {common.REPO_SETTINGS["has_issues"]: True, common.REPO_SETTINGS["allow_rebase_merge"]: False,
                   common.REPO_SETTINGS["delete_branch_on_merge"]: True}

defaults = org_repo_policy.copy()
defaults.update({common.REPO_SETTINGS["has_wiki"]: False, common.REPO_SETTINGS["has_projects"]: False,
                 common.REPO_SETTINGS["allow_squash_merge"]: True, common.REPO_SETTINGS["allow_merge_commit"]: True})


def check_policy(repo: github.Repository.Repository, policy: dict) -> bool:
    """
   Compare a series of settings to a GitHub repository

    :param repo: Repository to check
    :param policy: Mapping of settings and values to compare
    """
    policy_correct = True
    for k, v in policy.items():
        if getattr(repo, k) != v:
            print("POLICY VIOLATION - {} : {}".format(k, getattr(repo, k)))
            policy_correct = False

    return policy_correct


def setup_repo(repo: github.Repository.Repository, settings: dict) -> None:
    """
    Apply a series of settings to a GitHub repository

    :param repo: Repository to apply settings to
    :param settings: Mapping of settings and values to apply
    """
    repo.edit(**settings)

    branch = repo.get_branch(repo.default_branch)
    branch.edit_protection(require_code_owner_reviews=True, dismiss_stale_reviews=True,
                           required_approving_review_count=1, strict=True, contexts=[])


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Configure repository settings")
    parser.add_argument("-s", "--secret", required=True, help="GitHub token for authentication")
    parser.add_argument("-r", "--repo", required=True, help="The repository to inspect")
    parser.add_argument("-i", "--init", required=False, default=False, action='store_true',
                        help="Initialize repository to default settings")
    parser.add_argument("-f", "--enforce", required=False, default=False, action='store_true',
                        help="Enforce policy if repository has violations")

    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_args()

    github_client = github.Github(opts.secret)
    org = github_client.get_organization(common.GENAPSYS_GITHUB)
    target_repo = org.get_repo(opts.repo)

    if opts.init:
        print("Setting repo to initial default state")
        setup_repo(target_repo, defaults)

    policy_match = check_policy(target_repo, org_repo_policy)

    if opts.enforce and not policy_match:
        print("Policy violations found. Resetting to current policy")
        setup_repo(target_repo, org_repo_policy)
        policy_match = check_policy(target_repo, org_repo_policy)

    if not policy_match:
        sys.exit(1)

    sys.exit(0)
