#########################
Internal Actions Releases
#########################

*****
1.3.1
*****

  * Fixes the ``repo-configuration``'s handling of the ``--disable`` flag when passing it to the called action util

*****
1.3.0
*****

  * Adds the ``fork-check`` action
  * Adds the ``org-policies.yml`` reusable workflow with the intent to be used to apply org-wide policies to repositories throughout the organization. This workflow current runs the ``fork-check`` and ``repo-configuration`` actions when called, with conditional logic to determine flow based on the triggering event.
  * Adds ``run-org-policies.yml`` to run ``org-policies.yml`` within internal-actions

*****
1.2.0
*****

  * Adds ``repo-configuration`` action
  * Adds ``protect-tag`` option to ``increment-version`` action to protect the created tag from deletion or modification


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
