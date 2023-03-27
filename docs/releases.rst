#########################
Internal Actions Releases
#########################

*****
2.6.0
*****

  * Updates the ``pytest`` reusable action to invoke pytest via ``python -m coverage run -m pytest``, rather than ``python -m pytest --cov`` based on https://stackoverflow.com/questions/62221654/how-to-get-coverage-reporting-when-testing-a-pytest-plugin in order to support testing of pytest plugin packages.

*****
2.5.1
*****

  * Update versions of actions calls in the ``docker-build-push`` action to use versions that are not using deprecated actions

*****
2.5.0
*****

  * Add the ability for the ``setup-python`` reusable action to install specific python packages without using a requirements.txt file via the ``packages`` input.

*****
2.4.0
*****

  * Add ``api_exclude`` as an input to the ``build-docs`` action to exclude certain directories from being processed by ``sphinx-apidoc``

*****
2.3.0
*****

  * Add ``build-args`` input for build args for building docker images with the ``docker-build-push`` action

*****
2.2.1
*****

  * Exclude the ``build`` directory from ``mypy`` and ``pylint`` reusable actions and the ``static-analysis.yml`` reusable workflow to play nicer with src-layout packages that are being installed as part of the static analysis jobs

*****
2.2.0
*****

  * Adds the ``check-version`` action for version bump reminders when opening/updating pull requests

*****
2.1.1
*****

  * Updates the ``codeql``, ``docker-run``, and ``increment-version`` actions to address https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/

*****
2.1.0
*****

  * Adds ``mypy`` and ``pylint`` actions
  * Adds the ``static-analysis.yml`` reusable workflow

*****
2.0.0
*****

  * Changes the ``sonarqube`` reusable action to not actually run anything other than print a message informing the user that the SonarQube instance is down

*****
1.6.0
*****

  * Adds the ``workflow-templates`` directory with the intent of adding templates for workflows to be added in other repositories

*****
1.5.0
*****

  * Adds ``pytest-args`` option to ``pytest`` action to allow users to pass arguments to pytest

*****
1.4.0
*****

  * Allows user to supply a build command via the ``build-command`` input to the ``setup-python`` action which is executed as the final step of setup.  For example, this allows for the building of Cython modules prior to running unit tests downstream.
  * Added the install of wheel to the ``setup-python`` action in order to make the pip installs faster.


*****
1.3.1
*****

  * Fixes the ``repo-configuration`` action's handling of the ``--disable`` flag when passing it to the called action util

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
