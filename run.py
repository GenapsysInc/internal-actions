from action_utils.check_version import temp_name
import github
import os

secret = os.environ["GITHUB_SECRET"]

client = github.Github(secret)

temp_name(client, "GenapsysInc", "internal-actions")
