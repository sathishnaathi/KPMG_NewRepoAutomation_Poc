import os
import requests

GITHUB_TOKEN = os.getenv("REPO_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = "SathishDummy-Repo"

url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")
print(response.json())
