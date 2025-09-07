import os, requests

GITHUB_TOKEN = os.getenv("REPO_TOKEN")
headers = {
  "Authorization": f"Bearer {GITHUB_TOKEN}",
  "Accept": "application/vnd.github+json",
}

resp = requests.get("https://api.github.com/user", headers=headers)
print("Status:", resp.status_code, resp.json())

