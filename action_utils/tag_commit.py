"""Tag the current commit based on version information in a JSON file"""

__author__ = "David McConnell"
__credits__ = ["David McConnell"]
__maintainer__ = "David McConnell"

import argparse
import json

import git
import github

from action_utils import common


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Determine if relevant teams have approved a PR")

    parser.add_argument("-s", "--secret", required=True, help="GitHub token for authentication")

    parser.add_argument("-j", "--json", required=True, help="JSON file path")

    parser.add_argument("-d", "--date", action="store_true", required=False, help="Add a date string to the tag")

    return parser.parse_args()


if __name__ == '__main__':
    main()
