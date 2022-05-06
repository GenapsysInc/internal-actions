**********
Build Docs
**********

.. include:: ../../reusable-actions/build-docs/README.md
   :parser: myst_parser.sphinx_

Templates
=========

PR Template
-----------

Run the documentation but don't publish it.  This is good to check that the documents build without errors

.. include:: ../../reusable-actions/build-docs/pr-template.yml
   :parser: myst_parser.sphinx_
   :literal:

Push Template
-------------

Run the documentation and publish it.  This is good after the PR has been merged so that the published documents are always up-to-date.

.. include:: ../../reusable-actions/build-docs/pr-template.yml
   :parser: myst_parser.sphinx_
   :literal:
