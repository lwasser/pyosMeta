import os
from collections import defaultdict

import pandas as pd
import requests
from dotenv import load_dotenv

# GitHub repository information
repo_owner = "pyopensci"
repo_name = "software-submission"

load_dotenv()
token = os.environ["GITHUB_TOKEN"]

# API endpoint for issues
api_url = (
    f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?state=all"
)

# Initialize counters for issues per month
issues_per_month = defaultdict(int)

# Initialize lists to store issue details
issue_details = []

# Define headers with your personal access token
headers = {"Authorization": f"token {token}"}


def summarize_by_month(df):
    # Convert the "Date" column to datetime format
    df["date"] = pd.to_datetime(df["created-date"])

    # Extract the month and year into separate columns
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    # Group the DataFrame by month and year and count the issues
    summary = df.groupby(["year", "month", "issue_type"]).count().reset_index()

    summary.columns = ["year", "month", "type", "count"]
    print(summary.head())
    # Create a "month-year" column with the desired format
    summary["month-year"] = summary.apply(
        lambda row: f"{row['month']}-{row['year']}", axis=1
    )
    summary = summary.sort_values(by=["year", "month"])

    return summary


# Function to fetch issues from the GitHub API
def fetch_issues(api_url, headers):
    all_issues = []
    page = 1
    while True:
        response = requests.get(
            api_url, headers=headers, params={"page": page, "per_page": 100}
        )  # Increase per_page to a higher value
        if response.status_code == 200:
            issues = response.json()
            if not issues:
                break
            all_issues.extend(issues)
            page += 1
        else:
            print(
                f"Failed to fetch issues. Status code: {response.status_code}"
            )
            break
    return all_issues


# Fetch all issues from the repository
all_issues = fetch_issues(api_url, headers)

# Process the issues and store details in a DataFrame
for issue in all_issues:
    issue_title = issue["title"]
    issue_created_at = issue["created_at"]
    issue_labels = [label["name"] for label in issue["labels"]]

    # Skip issues with no label or help labels
    skip_issue = (
        len(issue_labels) == 0  # No labels
        or "help wanted" in map(str.lower, issue_labels)  # "help wanted" label
        or "help request"
        in map(str.lower, issue_labels)  # "Help Request" label
    )

    if not skip_issue:
        print("processing", issue["title"])

        # Check if the issue has the "presubmission" label
        is_presubmission = "0/presubmission" in map(str.lower, issue_labels)

        # Determine the type based on labels
        if is_presubmission:
            issue_type = "presubmission"
        else:
            issue_type = "submission"
        # Fetch the original labels when the issue was created
        original_labels = []
        events_url = issue["events_url"]
        response = requests.get(events_url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            for event in events:
                if (
                    event["event"] == "labeled"
                    and event["actor"]
                    and event["created_at"]
                ):
                    original_labels.append(
                        {
                            "label": event["label"]["name"],
                            "created_at": event["created_at"],
                        }
                    )

        issue_details.append(
            {
                "title": issue_title,
                "created-date": issue_created_at,
                "labels": ", ".join(issue_labels),
                "issue_type": issue_type,
            }
        )

print("Creating dataframe")
# Create a DataFrame from the issue details
issues_all = pd.DataFrame(issue_details)

# presubmit_df = df[df["Issue labels"].str.contains("0/presubmission")]

# Only presubmissions
# presubmit_df.to_csv("reviews_presubmissions.csv")
issues_all = issues_all.rename(columns={"Unnamed: 0": "id"})
issues_all.to_csv("reviews_all.csv")
issues_all = pd.read_csv("reviews_all.csv")
issues_all = issues_all.rename(columns={"Unnamed: 0": "id"})
print(issues_all.columns)

df = issues_all

# Convert the "Date" column to datetime format
df["date"] = pd.to_datetime(df["created-date"])

# Extract the month and year into separate columns
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Group the DataFrame by month and year and count the issues
summary = df.groupby(["year", "month", "issue_type"]).count().reset_index()

summary.columns = ["year", "month", "type", "count"]
print(summary.head())
# Create a "month-year" column with the desired format
summary["month-year"] = summary.apply(
    lambda row: f"{row['month']}-{row['year']}", axis=1
)
summary = summary.sort_values(by=["year", "month"])

# TODO: Running into some issues here...
summary = summarize_by_month(issues_all)
# Summarize

print("That's all folks")
