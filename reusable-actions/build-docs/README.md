# build-docs

This action will build the sphinx base documentation and if desired publish it to confluence and/or the repo's github pages. The expectation of the code is that the index and sphinx `conf.py` exist in the `/docs` dir. A version string to render in the HTML pages may optionally be passed in, which will override the version defined in the `conf.py`. This can be done in tandem with the `increment-version` action to have published docs reflect the latest tagged version of the repo.

## Build the docs but don't publish

```yaml

      - name: Documentation build and publish
        uses: GenapsysInc/internal-actions/reusable-actions/build-docs@main
        with:
          token: XXXXXXXXX
          confluence_secret: XXXXXXXXX
          build_confluence: true
          publish_confluence: false
          build_html: true
          publish_html: false
          warn_as_errors: false
          api_dirs: "code"
          api_exclude: "tests/**/data tests/bad_syntax/*.py"
          build_options: -n
```

## Build the HTML docs only

```yaml

      - name: Documentation build and publish
        uses: GenapsysInc/internal-actions/reusable-actions/build-docs@main
        with:
          token: XXXXXXXXX
          confluence_secret: XXXXXXXXX
          build_confluence: false
          publish_confluence: false
          build_html: true
          publish_html: true
          warn_as_errors: false
          api_dirs: "code"
          api_exclude: "tests/**/data tests/bad_syntax/*.py"
          build_options: -n
```

## Build and publish docs


```yaml

      - name: Documentation build and publish
        uses: GenapsysInc/internal-actions/reusable-actions/build-docs@main
        with:
          token: XXXXXXXXX
          confluence_secret: XXXXXXXXX
          build_confluence: true
          publish_confluence: true
          build_html: true
          publish_html: true
          warn_as_errors: false
          api_dirs: "code"
          api_exclude: "tests/**/data tests/bad_syntax/*.py"
          build_options: -n
```

## Tag new version and pass into the doc builder

```yaml

jobs:
  increment-version:
    runs-on: ubuntu-latest
    outputs:
      new-version: ${{ steps.run-increment-version.outputs.new-version }}
    steps:
      - name: Run the increment-version action
        id: run-increment-version
        uses: GenapsysInc/internal-actions/reusable-actions/increment-version@main
  doc-build:
    needs: increment-version
    runs-on: ubuntu-latest
    steps:
      - name: Documentation build and publish
        uses: GenapsysInc/internal-actions/reusable-actions/build-docs@main
        with:
          token: XXXXXXXXX
          confluence_secret: XXXXXXXXX
          build_confluence: true
          publish_confluence: true
          build_html: true
          publish_html: true
          warn_as_errors: false
          version: ${{ needs.increment-version.outputs.new-version }}
          api_dirs: "code"
          api_exclude: "tests/**/data tests/bad_syntax/*.py"
          build_options: -n
```
