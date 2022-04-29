# docker-run-action

Inspiration from https://github.com/addnab/docker-run-action/releases/tag/v3, converted to a composite action. This version differs in that a "shell" and "network" are not defined, as this caused the image's entrypoint to be overriden. Instead the defined entrypoint for the image is honored, and arguments can be passed to it via the `args` input. If an entrypoint override is desired, you can do so via the `options` input.

- Run a docker image pulled from a repository or built by a previous step
- See `action.yml` for available inputs

## Examples

#### Typical Use Case

```yaml
- name: Checkout
  uses: actions/checkout@v3 # Required to mount the Github Workspace to a volume
- uses: GenapsysInc/internal-actions/reusable-workflow/docker-run-action@main
  with:
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GHCR_TOKEN }}
    registry: ghcr.io
    image: ghcr.io/genapsysinc/private-image:latest
    options: -v ${{ github.workspace }}:/work -e ENV_VAR="hello"
```

#### Run an image built by a previous step
```yaml
- uses: docker/build-push-action@v2
  with:
    tags: test-image:latest
    push: false
- uses: GenapsysInc/internal-actions/reusable-workflow/docker-run-action@main
  with:
    image: test-image:latest
```

#### Pass arguments to an image
```yaml
- uses: GenapsysInc/internal-actions/reusable-workflow/docker-run-action@main
  with:
    image: docker:latest  # Has some pre-defined script running as the entrypoint
    args: <arg1> <arg2> <arg3> ...
```
