"""Unit tests for the action_utils.get_team_approval_status module"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import pytest

from action_utils import common
import action_utils.get_team_approval_status as gtas
import action_utils.tests.utils.pygithub_utils as pgh_utils


@pytest.fixture(name="user_1")
def fixture_user_1():
    return pgh_utils.MockGithubUser("Octocat")


@pytest.fixture(name="user_2")
def fixture_user_2():
    return pgh_utils.MockGithubUser("Angry github unicorn")


@pytest.fixture(name="user_3")
def fixture_user_3():
    return pgh_utils.MockGithubUser("BMO")


@pytest.fixture(name="user_4")
def fixture_user_4():
    return pgh_utils.MockGithubUser("Ein the dog")


@pytest.fixture(name="qa_team")
def fixture_qa_team(user_1, user_2, user_3):
    return pgh_utils.MockGithubTeam("QA", [user_1, user_2, user_3])


@pytest.fixture(name="devops_team")
def fixture_devops_team(user_2, user_3):
    return pgh_utils.MockGithubTeam("DevOps", [user_2, user_3])


@pytest.fixture(name="bioinformatics_team")
def fixture_bioinformatics_team(user_4):
    return pgh_utils.MockGithubTeam("Bioinformatics", [user_4])


@pytest.fixture(name="all_teams")
def fixture_all_teams(qa_team, devops_team, bioinformatics_team):
    return {team.name: team for team in [qa_team, devops_team, bioinformatics_team]}


@pytest.fixture(name="qa_approval")
def fixture_qa_approval(user_1):
    return pgh_utils.MockGithubReview(user_1, common.APPROVED)


@pytest.fixture(name="qa_comment")
def fixture_qa_comment(user_1):
    return pgh_utils.MockGithubReview(user_1, common.COMMENTED)


@pytest.fixture(name="qa_change_request")
def fixture_qa_change_request(user_1):
    return pgh_utils.MockGithubReview(user_1, common.CHANGES_REQUESTED)


@pytest.fixture(name="devops_approval")
def fixture_devops_approval(user_2):
    return pgh_utils.MockGithubReview(user_2, common.APPROVED)


@pytest.fixture(name="devops_comment")
def fixture_devops_comment(user_2):
    return pgh_utils.MockGithubReview(user_2, common.COMMENTED)


@pytest.fixture(name="devops_change_request")
def fixture_devops_change_request(user_2):
    return pgh_utils.MockGithubReview(user_2, common.CHANGES_REQUESTED)


@pytest.fixture(name="bioinformatics_approval")
def fixture_bioinformatics_approval(user_4):
    return pgh_utils.MockGithubReview(user_4, common.APPROVED)


@pytest.fixture(name="bioinformatics_comment")
def fixture_bioinformatics_comment(user_4):
    return pgh_utils.MockGithubReview(user_4, common.COMMENTED)


@pytest.fixture(name="bioinformatics_change_request")
def fixture_bioinformatics_change_request(user_4):
    return pgh_utils.MockGithubReview(user_4, common.CHANGES_REQUESTED)


@pytest.fixture(name="pull_all_teams_approved")
def fixture_pull_all_teams_approved(qa_approval, devops_approval, bioinformatics_approval):
    return pgh_utils.MockGithubPull(1, [qa_approval, devops_approval, bioinformatics_approval])


@pytest.fixture(name="pull_all_teams_commented")
def fixture_pull_all_teams_commented(qa_comment, devops_comment, bioinformatics_comment):
    return pgh_utils.MockGithubPull(2, [qa_comment, devops_comment, bioinformatics_comment])


@pytest.fixture(name="pull_all_teams_requested_changes")
def fixture_pull_all_teams_requested_changes(qa_change_request, devops_change_request, bioinformatics_change_request):
    return pgh_utils.MockGithubPull(3, [qa_change_request, devops_change_request, bioinformatics_change_request])


@pytest.fixture(name="pull_mixed_reviews")
def fixture_pull_mixed_reviews(qa_change_request, devops_approval, bioinformatics_approval):
    return pgh_utils.MockGithubPull(4, [qa_change_request, devops_approval, bioinformatics_approval])


@pytest.fixture(name="pull_qa_recent_approval_1")
def fixture_pull_qa_recent_approval_1(qa_approval, qa_comment, qa_change_request):
    return pgh_utils.MockGithubPull(5, [qa_change_request, qa_comment, qa_comment, qa_approval])


@pytest.fixture(name="pull_qa_recent_approval_2")
def fixture_pull_qa_recent_approval_2(qa_approval, qa_comment, qa_change_request):
    return pgh_utils.MockGithubPull(6, [qa_change_request, qa_comment, qa_approval, qa_comment])


@pytest.fixture(name="pull_qa_recent_change_request_1")
def fixture_pull_qa_recent_change_request_1(qa_approval, qa_comment, qa_change_request):
    return pgh_utils.MockGithubPull(7, [qa_approval, qa_comment, qa_comment, qa_change_request])


@pytest.fixture(name="pull_qa_recent_change_request_2")
def fixture_pull_qa_recent_change_request_2(qa_approval, qa_comment, qa_change_request):
    return pgh_utils.MockGithubPull(8, [qa_approval, qa_comment, qa_change_request, qa_comment])


@pytest.fixture(name="test_repo")
def fixture_test_repo(
    pull_all_teams_approved,
    pull_all_teams_commented,
    pull_all_teams_requested_changes,
    pull_mixed_reviews,
    pull_qa_recent_approval_1,
    pull_qa_recent_approval_2,
    pull_qa_recent_change_request_1,
    pull_qa_recent_change_request_2,
):
    all_pulls = [
        pull_all_teams_approved,
        pull_all_teams_commented,
        pull_all_teams_requested_changes,
        pull_mixed_reviews,
        pull_qa_recent_approval_1,
        pull_qa_recent_approval_2,
        pull_qa_recent_change_request_1,
        pull_qa_recent_change_request_2,
    ]

    return pgh_utils.MockGithubRepo("my-repo", pulls={pull.num: pull for pull in all_pulls})


@pytest.fixture(name="test_org")
def fixture_test_org(all_teams, test_repo):
    return pgh_utils.MockGithubOrg(common.GENAPSYS_GITHUB, teams=all_teams, repos={test_repo.name: test_repo})


@pytest.fixture(name="authenticated_client")
def fixture_authenticated_client(test_org):
    return pgh_utils.MockGithubClient({test_org.name: test_org}, authenticated=True)


@pytest.fixture(name="unauthenticated_client")
def fixture_unauthenticated_client(test_org):
    return pgh_utils.MockGithubClient({test_org.name: test_org}, authenticated=False)


class TestTeamMemberHasApprovedPR:
    """Tests for the team_member_has_approved_pr function"""

    @staticmethod
    def test_true_all(qa_team, pull_all_teams_approved):
        """All teams have approved, so QA should be marked as having approved"""
        assert gtas.team_member_has_approved_pr(qa_team, pull_all_teams_approved)

    @staticmethod
    def test_true_mixed_team(qa_team, pull_mixed_reviews):
        """Case where 1 QA team member has not approved but another has, QA should be marked as having approved"""
        assert gtas.team_member_has_approved_pr(qa_team, pull_mixed_reviews)

    @staticmethod
    def test_true_multiple_reviews_1(qa_team, pull_qa_recent_approval_1):
        """QA previously requested changes, but the most recent review is an approval, should be marked as approved"""
        assert gtas.team_member_has_approved_pr(qa_team, pull_qa_recent_approval_1)

    @staticmethod
    def test_true_multiple_reviews_2(qa_team, pull_qa_recent_approval_2):
        """QA previously requested changes, but the most recent was an approval, should be marked as approved"""
        assert gtas.team_member_has_approved_pr(qa_team, pull_qa_recent_approval_2)

    @staticmethod
    def test_false_comment(qa_team, pull_all_teams_commented):
        """All teams have only commented, QA should not be marked as having approved"""
        assert not gtas.team_member_has_approved_pr(qa_team, pull_all_teams_commented)

    @staticmethod
    def test_false_change_request(qa_team, pull_all_teams_requested_changes):
        """All teams have only requested changes, QA should not be marked as having approved"""
        assert not gtas.team_member_has_approved_pr(qa_team, pull_all_teams_requested_changes)

    @staticmethod
    def test_false_multiple_reviews_1(qa_team, pull_qa_recent_change_request_1):
        """QA previously approved, but the most recent review is a change request, should not be marked as approved"""
        assert not gtas.team_member_has_approved_pr(qa_team, pull_qa_recent_change_request_1)

    @staticmethod
    def test_false_multiple_reviews_2(qa_team, pull_qa_recent_change_request_2):
        """QA previously approved, but the most recent was a change request, should not be marked as approved"""
        assert not gtas.team_member_has_approved_pr(qa_team, pull_qa_recent_change_request_2)


class TestPRHasAppropriateReviews:
    """Tests for the pr_has_appropriate_reviews function"""

    @staticmethod
    def test_pr_has_appropriate_reviews_true_all(authenticated_client, test_repo, pull_all_teams_approved, all_teams):
        """End-to-end style test for when a PR has required team approvals"""
        assert gtas.pr_has_appropriate_reviews(
            authenticated_client, test_repo.name, pull_all_teams_approved.num, all_teams
        )

    @staticmethod
    def test_pr_has_appropriate_reviews_true_mixed(authenticated_client, test_repo, pull_mixed_reviews, all_teams):
        """End-to-end style test for when a PR has some change requests and some approvals but meets overall approval"""
        assert gtas.pr_has_appropriate_reviews(authenticated_client, test_repo.name, pull_mixed_reviews.num, all_teams)

    @staticmethod
    def test_pr_has_appropriate_reviews_false_comments(
        authenticated_client, test_repo, pull_all_teams_commented, all_teams
    ):
        """End-to-end style test for when a PR has only comments"""
        assert not gtas.pr_has_appropriate_reviews(
            authenticated_client, test_repo.name, pull_all_teams_commented.num, all_teams
        )

    @staticmethod
    def test_pr_has_appropriate_reviews_false_changes_requested(
        authenticated_client, test_repo, pull_all_teams_requested_changes, all_teams
    ):
        """End-to-end style test for when a PR has only change requests"""
        assert not gtas.pr_has_appropriate_reviews(
            authenticated_client, test_repo.name, pull_all_teams_requested_changes.num, all_teams
        )

    @staticmethod
    def test_pr_has_appropriate_reviews_false_mixed(
        authenticated_client, test_repo, pull_qa_recent_approval_1, all_teams
    ):
        """End-to-end style test for when a PR has some change requests and some approvals but meets overall approval"""
        assert not gtas.pr_has_appropriate_reviews(
            authenticated_client, test_repo.name, pull_qa_recent_approval_1.num, all_teams
        )

    @staticmethod
    def test_pr_has_appropriate_reviews_authentication_fail(
        unauthenticated_client, test_repo, pull_all_teams_approved, all_teams
    ):
        """End-to-end style test to assert proper handling of authentication failure"""
        with pytest.raises(common.ConfigurationError):
            gtas.pr_has_appropriate_reviews(
                unauthenticated_client, test_repo.name, pull_all_teams_approved.num, all_teams
            )

    @staticmethod
    def test_pr_has_appropriate_reviews_invalid_repo(authenticated_client, pull_all_teams_approved, all_teams):
        """End-to-end style test to assert proper handling of invalid repo"""
        with pytest.raises(common.ConfigurationError):
            gtas.pr_has_appropriate_reviews(authenticated_client, "not-a-repo", pull_all_teams_approved.num, all_teams)

    @staticmethod
    def test_pr_has_appropriate_reviews_invalid_pull(authenticated_client, test_repo, all_teams):
        """End-to-end style test to assert proper handling of invalid PR number"""
        with pytest.raises(common.ConfigurationError):
            gtas.pr_has_appropriate_reviews(authenticated_client, test_repo, 10000, all_teams)

    @staticmethod
    def test_pr_has_appropriate_reviews_missing_teams(authenticated_client, test_repo, pull_all_teams_approved):
        """End-to-end style test to assert proper handling of invalid team name"""
        with pytest.raises(common.ConfigurationError):
            gtas.pr_has_appropriate_reviews(
                authenticated_client, test_repo, pull_all_teams_approved.num, ["not-a-team"]
            )
