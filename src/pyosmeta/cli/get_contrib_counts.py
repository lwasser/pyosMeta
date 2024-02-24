"""
A script that parses current contributors and updates total counts including:
* total contribs
* total_maintainers
* total_reviewers
* total_editors

Also returns:
* current date

"""

import pickle 

from pyosmeta import ProcessIssues, ReviewModel

# Open pickle file w contribs
with open("all_contribs.pickle", "rb") as f:
    contrib_dict = pickle.load(f)

# Get total maintainer counts

types = ["maintainer", "reviewer", "editor"]
# Initialize a dictionary to store counts for each type
type_counts = {contrib_type: 0 for contrib_type in types}

# Count the number of people for each type
total_people = 0
for person in contrib_dict.values():
    total_people +=1
    for contrib_type in types:
        counted_people = set()
        if contrib_type in person.contributor_type and person.name not in counted_people:
            type_counts[contrib_type] += 1
            counted_people.add(person.name)

type_counts["total_people"] = total_people
print(type_counts)

# Get review counts

