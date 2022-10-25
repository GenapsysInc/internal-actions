# pylint

This action will set up python, install requirements, and then run pylint. Passing checks are gated by any settings defined in pylint's configuration. By default, pylint runs in the root directory of the repo, ignoring the `docs` and `confluence` directories, which may be present for doc building. The arguments to pylint may be overridden by supplying a `args` input to the action.

This action will use a `pylintrc` (or `.pylintrc`, `pyproject.toml`, or `setup.cfg`) file in the root directory of the calling repository to configure how pylint runs. See https://pylint.pycqa.org/en/latest/user_guide/usage/run.html#command-line-options.

This action can be called independently or called via the `internal-actions/.github/workflows/static-analysis.yml` reusable workflow.
