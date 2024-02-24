from pyosmeta import ProcessIssues

import os 
from github import Github
from dotenv import load_dotenv

labels_dict = {
    'label_onhold': ["⌛ pending-maintainer-response", "on-hold"],
    'label_in_review': [
        "1/editor-checks",
        "2/seeking-reviewer(s)",
        "3/reviewer(s)-assigned",
        "4/review(s)-in-awaiting-changes",
        "5/awaiting-reviewer(s)-response"
    ],
    'label_approved': ["6/pyOS-approved 🚀🚀🚀", "9/joss-approved"],
    'label_out_of_scope':["currently-out-of-scope"]
}

load_dotenv()
github_token = os.environ.get('GITHUB_TOKEN')
# Initialize PyGithub by providing your personal access token
g = Github(github_token)

# Get the repository
repo = g.get_repo("pyopensci/software-submission")

# Fetch issues with pagination
issues = repo.get_issues(state="all")


# Iterate over the issues

for i, issue in enumerate(issues):
    print(issue.title)

print("there are ", i+1, "total issues")