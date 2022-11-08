# check-version

This action will inspect the changed files in a pull request and inspect a JSON file with version information to determine if the configured version should have been bumped but was not in a given pull request. It will create a comment on the pull request reminding the author to update the version if it thinks a bump is needed. A list of directories, file names, or patterns to include for the check, and ones to exclude for the check can be submitted as a list of space-delimited strings. This action will *not* gate pull request merges, its purpose is only to act as a reminder.
