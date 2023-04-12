import requests
from requests.auth import HTTPBasicAuth
import json
import os
import re

# Get the value of an environment variable
issue_id = os.environ.get('ISSUE')
username = os.environ.get('JIRA_USERNAME')
token = os.environ.get('JIRA_API_TOKEN')
jira_url = os.environ.get('JIRA_BASE_URL')
pr_url = os.environ.get('PULL_REQUEST_URL')

jira_ticket_pattern = r"[A-Z]+\-\d+"
matches = re.findall(jira_ticket_pattern, issue_id)

for word in matches:
    url = jira_url+"/rest/api/3/issue/"+word+"/comment"
    print(url)
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
                "text": pr_url,
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
