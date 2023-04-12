import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Get the value of an environment variable
issue_id = os.environ.get('ISSUE')
username = os.environ.get('JIRA_USERNAME')
token = os.environ.get('JIRA_API_TOKEN')
words = issue_id.split()

for word in words:
    if word.startswith("#"):
        url = "https://kaleyra.atlassian.net/rest/api/3/issue/"+word[1:]+"/comment"
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
                    "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget venenatis elit. Duis eu justo eget augue iaculis fermentum. Sed semper quam laoreet nisi egestas at posuere augue semper.",
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
