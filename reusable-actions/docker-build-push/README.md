# docker-build-push

This action builds and optionally pushes a docker image. When given a registry, username, and password, it will authenticate to the registry to allow pulling private base images for builds, or pushing built images to a private registry. The action also caches docker layers across multiple runs to allow for docker to cache the way it was meant to. To use a built image in a subsequent step, the `load` flag must be set to `true`. See `action.yml` for available inputs.

#### Build and load an image, use it in subsequent steps
```yaml
- name: Build and load an image
  uses: GenapsysInc/internal-actions/reusable-actions/docker-build-push@main
  with:
    context: .
    dockerfile: path/to/Dockerfile
    load: true
    tags: my-image:latest
- name: Run the built image
  uses: GenapsysInc/internal-actions/reusable-actions/docker-run@main
  with:
    image: my-image:latest
```

#### Build and push an image
```yaml
- name: Build and push an image
  uses: GenapsysInc/internal-actions/reusable-actions/docker-build-push@main
  with:
    context: .
    dockerfile: path/to/Dockerfile
    push: true
    tags: my-image:latest
```

#### Build and push an image to a private repository
```yaml
- name: Build and load an image, authenticate to ghcr.io
  uses: GenapsysInc/internal-actions/reusable-actions/docker-build-push@main
  with:
    context: .
    dockerfile: path/to/Dockerfile
    push: true
    tags: ghcr.io/genapsysinc/my-image:latest
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GHCR_TOKEN }}
```
