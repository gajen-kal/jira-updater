import requests
from requests.auth import HTTPBasicAuth
import json
import os
import re
import json

# Get the value of an environment variable
issue_id = os.environ.get('ISSUE')
username = os.environ.get('JIRA_USERNAME')
token = os.environ.get('JIRA_API_TOKEN')
jira_url = os.environ.get('JIRA_BASE_URL')
pr_url = os.environ.get('PULL_REQUEST_URL')
pr_branch = os.environ.get('PR_BRANCH')
git_token = os.environ.get('GIT_TOKEN')
pr_number = os.environ.get('PR_NUMBER')

url = "https://api.github.com/repos/kaleyra/rbac/pulls/"+pr_number
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer "+git_token,
    "X-GitHub-Api-Version": "2022-11-28"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the response to get the SHA of the head commit
    data = json.loads(response.text)
    sha = data["head"]["sha"]
    # Make another request to the API to get the commits
    url = f"https://api.github.com/repos/kaleyra/rbac/commits?sha={sha}"
    response = requests.get(url, headers=headers)

    # Parse the response to get the commit messages
    data = json.loads(response.text)
    for commit in data:
        message = commit["commit"]["message"]
        print(message)
else:
    print(f"Error {response.status_code}: {response.text}")


jira_ticket_pattern = r"[A-Z0-9]+-\d+"
matches = re.findall(jira_ticket_pattern, issue_id)

for word in matches:
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
                "text": "pull request url : "+pr_url,
                "type": "text"
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
