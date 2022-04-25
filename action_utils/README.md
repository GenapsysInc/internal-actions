## Action Utils

This directory contains scripts/modules intended to be used as utilities in different github actions defined within the internal-actions repository. Scripts performing checks that would gate a pull request merge should exit with an exit code of 0 when criteria are met, and 1 otherwise. One python requirements file is used to define 3rd party library dependencies across the suite of utils. Unit tests should be added to the tests sub-directory. Tests will run using Python3.7 and Python3.10.
