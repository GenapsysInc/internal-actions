## Team Approval Docker Image

This docker image will take as input a repository, pull request ID, and list of team names and determine if the PR has approvals from at least 1 member of each team. This docker image is intended to be run in the context of a github action to gate pull requests behind appropriate reviews across different teams in Digital Science.

### Building the image

From `internal-actions`, intended to be pushed up to ghcr.io:
```
docker build . -f team_approval/Dockerfile -t ghcr.io/genapsysinc/team-approval:latest
```

On a merge to main, this process will happen automatically

### Running the image

```
docker run ghcr.io/genapsysinc/team_approval:latest -s <github_secret> -r <repo> -p <pull_request_id> -t <team_1> <team_2> ...
```

If the appropriate teams have approved the pull request, the process will exit with a code of 0. If not, the image will exit with a code of 1.

### Updating the image

#. Increment the version listed at the top of this README
#. Change the version specified in the github action under `.github/workflows`
#. If adding yum or python package dependencies, update the yum-requirements.txt and python-requirements.txt files, respectively