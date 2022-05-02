#build-docs

This action will build the sphinx base documentation and if desired publish it to confluence and/or the repo's github pages.  The expectation of the code is that the index and sphinx conf.py exist in the `/docs` dir. 

#### Build the docs but don't publish

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
```

#### Build the HTML docs only 

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
```

#### Build and publish docs

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
```