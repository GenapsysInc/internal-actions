# submodule-check

This action will assert that the calling repository's submodules are all on commits in the default branch's commit history for each respective submodule. Essentially requires submodules to be on a "prod-ready" commit to be merged. This action is intended to be used to gate pull requests where the repository's default branch is the base branch in the pull request.
