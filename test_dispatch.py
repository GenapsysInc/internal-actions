import os

import github

client = github.Github(os.environ["GITHUB_SECRET"])

workflows = client.get_organization("genapsysinc").get_repo("internal-actions").get_workflows()

for workflow in workflows:
    print(workflow)