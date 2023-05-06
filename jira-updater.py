import requests
from requests.auth import HTTPBasicAuth
import json
import os
import re
import json
import subprocess

# Get the value of an environment variable
issue_id = os.environ.get('ISSUE')
username = os.environ.get('JIRA_USERNAME')
token = os.environ.get('JIRA_API_TOKEN')
jira_url = os.environ.get('JIRA_BASE_URL')
pr_url = os.environ.get('PULL_REQUEST_URL')
pr_title = os.environ.get('PR_MESSAGE')
pr_branch = os.environ.get('PR_BRANCH')
git_token = os.environ.get('GIT_TOKEN')
pr_number = os.environ.get('PR_NUMBER')
repo_name = os.environ.get('REPO_NAME')
target_branch = os.environ.get('TARGET_BRANCH')
commit_message = os.environ.get('COMMIT_MESS')
trigger_event = os.environ.get('TRIGGER_EVENT')
commit_id = os.environ.get('COMMIT_ID')
print(f"THE TRIGGER EVENT IS: {trigger_event}")
print(trigger_event)
print(commit_id)
# url = "https://api.github.com/repos/"+repo_name+"/pulls/"+pr_number
# headers = {
#     "Accept": "application/vnd.github+json",
#     "Authorization": "Bearer "+git_token,
#     "X-GitHub-Api-Version": "2022-11-28"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     # Parse the response to get the SHA of the head commit
#     data = json.loads(response.text)
#     sha = data["head"]["sha"]
#     print(sha)
#     # Make another request to the API to get the commits
#     url = f"https://api.github.com/repos/{repo_name}/commits?sha={sha}"
#     response = requests.get(url, headers=headers)

#     # Parse the response to get the commit messages
#     data = json.loads(response.text)
#     for commit in data:
#         message = commit["commit"]["message"]
#         print(message)
# else:
#     print(f"Error {response.status_code}: {response.text}")
if trigger_event == "pull_request":
    # Run the git log command and capture its output
    pr_output = subprocess.check_output(["git", "log", "--pretty=format:%s", f"origin/{pr_branch}"])

    # Decode the output as a string
    pr_output_string = pr_output.decode("utf-8")

    pr_commit_mssg=pr_output_string.split("\n")

    # Run the git log command and capture its output
    target_output = subprocess.check_output(["git", "log", "--pretty=format:%s", f"origin/{target_branch}"])

    # Decode the output as a string
    target_output_string = target_output.decode("utf-8")

    target_commit_mssg=target_output_string.split("\n")

    res = [item for item in pr_commit_mssg if item not in target_commit_mssg]
    res.append(issue_id)

    # Convert the list to a string with comma as separator
    issue_string = ', '.join(res)
    url = pr_url
else:
    issue_string = commit_message
    url = "https://github.com/kaleyra/billing/commit/"+commit_id
print(issue_string)

# Regular expression for jira ticket
jira_ticket_pattern = r"[A-Z0-9]+-\d+"

# Find the ticket ids
matches = re.findall(jira_ticket_pattern, issue_string)

# Convert the list to a set to remove duplicates
issue_list = list(set(matches))

print(issue_list)
print(matches)

for word in issue_list:
    url = jira_url+"/rest/api/3/issue/"+word+"/comment"
    auth = HTTPBasicAuth(username, token)

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    payload = json.dumps( {
      "body": {
        "content": [
          {
            "content": [
              {
                "text": pr_title,
                "type": "text",
                "text": url,
                "type": "text",
                "marks": [
                  {
                    "type": "link",
                    "attrs": {
                      "href": url,
                      "title": "Pull Request"
                    }
                   }
                ]
              }
            ],
            "type": "paragraph"
          }
        ],
        "type": "doc",
        "version": 1
      }
    } )

    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
