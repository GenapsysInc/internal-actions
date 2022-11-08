# Makefile framework

# Sphinx vars
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = _build


# Make commands
HELP_TEXT  = "\nDocumentation\n********************\n\n\nTargets\n=======\n\n"
HELP_TEXT += $(__TARGET_HELP)

CWD := ${CURDIR}

# Put it first so that "make" without argument is like "make help".
.PHONY: help
help:
	@echo $(HELP_TEXT) $(VAR_TEXT)

clean:
	rm -rf _builder confluence doctrees docs/_*

.PHONY: api-docs Makefile
__TARGET_HELP += "  * api-docs - Generates the rst documentation for all code in the \`action_utils/\` directory\n"
api-docs:
	docker pull ghcr.io/genapsysinc/docbuilder:latest
	docker run -v `pwd`:/repo/ ghcr.io/genapsysinc/docbuilder:latest -d action_utils

__TARGET_HELP += "  * html - Build the html documentation locally.  The \`index.html\` is in the \`$(BUILDDIR)/html/\` directory\n"
html:
	docker pull ghcr.io/genapsysinc/docbuilder:latest
	docker run -v `pwd`:/repo/ ghcr.io/genapsysinc/docbuilder:latest -m -d action_utils

__TARGET_HELP += "  * confluence - Build the confluence documentation.\n"
confluence:
	docker pull ghcr.io/genapsysinc/docbuilder:latest
	docker run -v `pwd`:/repo/ ghcr.io/genapsysinc/docbuilder:latest -c -d action_utils

__TARGET_HELP += "  * test - Run pytest and produce term-missing coverage report\n"
test:
	python3 -m pytest --cov-report=term-missing --cov=action_utils

__TARGET_HELP += "  * mypy - Run mypy, ignoring docs and confluence dirs\n"
mypy:
	mypy --exclude docs --exclude confluence .

__TARGET_HELP += "  * pylint - Run pylint, ignoring docs and confluence dirs\n"
pylint:
	pylint --ignore docs,confluence --recursive=true .
