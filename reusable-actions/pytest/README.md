# pytest

This action will set up python, install requirements, and then run pytest with code coverage capture turned on and reported in XML format. The test result and code coverage files will be uploaded as an artifact called `test-reports` and can be used by subsequent jobs/steps.

This action will use a `.coveragerc` (or `pyproject.toml`, `setup.cfg`, or `tox.ini`) in the root directory of the calling repository to configure coverage running and reporting. Information in the configuration file will define the set of files that will have coverage information captured. See https://coverage.readthedocs.io/en/6.3.2/source.html for more information about source file configuration. Note that `relative_files` should be set to `True` to integrate a coverage report into another tool like SonarQube, in which the absolute path of where files exist might be different. An example `.coveragerc` is included in this directory to be used if wanted.

This action can be called independently but is intended to be used as part of the `internal-actions/reusable-actions/sonarqube` action for test result and coverage report integration in a Sonar project. An example template for running pytest followed by SonarQube is included in that action's directory.
