# sonarqube

This action runs the SonarQube workflow when given a SonarQube token and URL. These are preconfigured at the organization level as GitHub secrets but must be passed by the calling workflow. There is a preconfigured template in this directory that can be used as is, with the exception of updating branches to run the workflow on (should be at least the default branch of the repository).

Currently the template also runs pytest and passes on code coverage to SonarQube. If this is not desired (although it is recommended), remove/comment out the `run-unit-tests` job and remove/comment out the `needs: run-unit-tests` line from the `run-sonarqube` job. An example `.coveragerc` file for code coverage integration lives in `internal-actions/reusable-actions/pytest`. Integration for testing code written in other languages will be added sometime soon.
