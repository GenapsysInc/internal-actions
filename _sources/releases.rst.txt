#########################
Internal Actions Releases
#########################

*****
1.1.0
*****

  * Adds the ``codeql`` action and an example template, intended for use when using CodeQL in a multi-job workflow as opposed to a standalone workflow
  * Adds a ``new-version`` output to the ``increment-version`` action for use in subsequent steps/jobs
  * Error handling in the ``actions_utils/tag_commit.py`` module for when trying to lay down a tag that already exists, which can happen when the local git workspace hasn't pulled down recent tags
  * Adds a ``version`` input to the ``build-docs`` action, which will override the version in the ``conf.py`` when building HTML docs
  * Consolidates existing workflows into a single, multi-job ``repo-jobs.yml`` workflow, allowing for easier and more explicit inter-job dependencies for the ``internal-actions`` repository

*****
1.0.0
*****

  * First official release of ``internal-actions``. Includes the following actions in a "prod-ready" state:

    * ``build-docs``
    * ``docker-build-push``
    * ``docker-run``
    * ``increment-version``
    * ``pytest``
    * ``setup-python``
    * ``sonarqube``
    * ``submodule-check``
    * ``team-approval``
