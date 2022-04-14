## Team Approval Docker Image

**Version 1**

This docker image will take as input a repository, pull request ID, and list of team names and determine if the PR has approvals from at least 1 member of each team. This docker image is intended to be run in the context of a github action to gate pull requests behind appropriate reviews across different teams in Digital Science.

### Building the image

From `internal-actions`:
```
docker build . -f team_approval/Dockerfile -t team_approval:v<version>
```

### Running the image

```
docker run team_approval:<version> -s <github_secret> -r <repo> -p <pull_request_id> -t <team_1> <team_2> ...
```

If the appropriate teams have approved the pull request, the process will exit with a code of 0. If not, the image will exit with a code of 1.

### Updating the image

#. Increment the version listed at the top of this README
#. Change the version specified in the github action under `.github/workflows`
