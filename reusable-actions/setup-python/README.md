## setup-python action

This action is intended to be used by other actions/workflows to setup a given python environment. It will run python setup (default is version 3.10), install python requirements given a requirements.txt file path, and cache dependency installation appropriately. Wildcards may be used for the path to the requirements.txt file(s).


#### Setup Python 3.10

```yaml
- name: Install and set up Python 3.10
  uses: GenapsysInc/internal-actions/reusable-actions/setup-python@main
```

#### Setup Python 3.x

```yaml
- name: Install and set up Python 3.x
  uses: GenapsysInc/internal-actions/reusable-actions/setup-python@main
  with:
    python-version: 3.x
```

#### Install Specific Python Dependencies

```yaml
- name: Checkout source tree
  uses: actions/checkout@v3
- name: Install and set up Python 3.10 and install dependencies
  uses: GenapsysInc/internal-actions/reusable-actions/setup-python@main
  with:
    requirements-txt: path/to/requirements.txt
```

#### Install Wildcard Python Dependencies

```yaml
- name: Checkout source tree
  uses: actions/checkout@v3
- name: Install and set up Python 3.10 and install dependencies
  uses: GenapsysInc/internal-actions/reusable-actions/setup-python@main
  with:
    requirements-txt: **/requirements.txt
```
