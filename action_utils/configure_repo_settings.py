"""Configure and check repository settings"""

__author__ = "Aaron Berlin"

import argparse
import sys

from ghapi.all import GhApi, print_summary

from action_utils import common

# TODO: figure out why the policy won't correct itself - likely missing a required setting in the blob
org_repo_policy = {common.REPO_SETTINGS["has_issues"]: True, common.REPO_SETTINGS["allow_rebase_merge"]: False,
                   common.REPO_SETTINGS["delete_branch_on_merge"]: True}

defaults = org_repo_policy.copy()
defaults.update({common.REPO_SETTINGS["has_wiki"]: False, common.REPO_SETTINGS["has_projects"]: False,
                 common.REPO_SETTINGS["allow_squash_merge"]: True, common.REPO_SETTINGS["allow_merge_commit"]: True})

default_branch_protections = {common.BRANCH_PROTECTION["enforce_admins"]: False,
                              common.BRANCH_PROTECTION["required_conversation_resolution"]: True,
                              common.BRANCH_PROTECTION["restrictions"]: {"users": [], "teams": []},
                              common.BRANCH_PROTECTION["required_pull_request_reviews"]: {
                                  common.BRANCH_PROTECTION["dismiss_stale_reviews"]: True,
                                  common.BRANCH_PROTECTION["require_code_owner_reviews"]: True,
                                  common.BRANCH_PROTECTION["required_approving_review_count"]: 1,
                              },
                              common.BRANCH_PROTECTION["required_status_checks"]: {
                                  common.BRANCH_PROTECTION["require_branches_uptodate"]: True,
                                  common.BRANCH_PROTECTION["required_passing_checks"]: []}
                              }


def check_policy(connection: GhApi, policy: dict) -> bool:
    """
    Compare a series of settings to a GitHub repository

    :param connection: GitHub API connection to repository
    :param policy: Mapping of settings and values to compare
    """
    policy_correct = True
    repo_details = connection.repos.get()

    for k, v in policy.items():
        if getattr(repo_details, k) != v:
            print("POLICY VIOLATION - {} : {}".format(k, getattr(repo_details, k)))
            policy_correct = False

    return policy_correct


def setup_repo(connection: GhApi, settings: dict, branch_protections: dict = None) -> None:
    """
    Apply a series of settings to a GitHub repository

    :param connection: GitHub API connection to repository
    :param settings: Mapping of settings and values to apply
    :param branch_protections: Mapping of settings and values to use top protected the default branch - optional
    """

    repo_details = connection.repos.get()
    default_branch = repo_details["default_branch"]
    connection.repos.update(**settings)

    if branch_protections:
        connection.repos.update_branch_protection(branch=default_branch, **branch_protections)

    connection.enable_pages(branch='gh-pages', path='/')
    pages_url = connection.repos.get_pages()["html_url"]
    connection.repos.update(description=pages_url)


def disable_action(connection: GhApi, run_id: str) -> None:

    work_id = connection.actions.get_workflow_run(run_id)["workflow_id"]
    connection.actions.disable_workflow(workflow_id=work_id)


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Configure repository settings")
    parser.add_argument("-s", "--secret", required=True, help="GitHub token for authentication")
    parser.add_argument("-r", "--repo", required=True, help="The repository to inspect")
    parser.add_argument("-i", "--init", required=False, default=False, action='store_true',
                        help="Initialize repository to default settings")
    parser.add_argument("-d", "--debug", required=False, default=False, action='store_true',
                        help="Print API preview calls for debugging")
    parser.add_argument("-f", "--enforce", required=False, default=False, action='store_true',
                        help="Enforce policy if repository has violations")
    parser.add_argument("--disable", required=False, help="Disable the action calling this - Only for GH Action calls")
    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_args()

    api = GhApi(common.GENAPSYS_GITHUB, repo=opts.repo, token=opts.secret)
    if opts.debug:
        api.debug = print_summary

    if opts.init:
        print("Setting repo to initial default state")
        setup_repo(api, defaults, default_branch_protections)

    policy_match = check_policy(api, org_repo_policy)

    if opts.enforce and not policy_match:
        print("Policy violations found. Resetting to current policy")
        setup_repo(api, org_repo_policy, default_branch_protections)
        policy_match = check_policy(api, org_repo_policy)

    if opts.disable:
        disable_action(api, opts.disable)

    if not policy_match:
        sys.exit(1)

    sys.exit(0)
