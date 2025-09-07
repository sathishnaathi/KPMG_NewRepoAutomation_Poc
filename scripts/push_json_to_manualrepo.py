import os
import json
import base64
import requests

# Configuration
GITHUB_TOKEN = os.getenv("REPO_TOKEN")  # GitHub token passed via environment
REPO_OWNER = os.getenv("REPO_USER")              # Replace with actual GitHub username/org that owns sathishdummy-repo
REPO_NAME = "SathishDummy-Repo"
FILE_PATH = "data.json"
BRANCH = "main"                           # Change if pushing to a different branch
COMMIT_MESSAGE = "Automated: Add dummy JSON file from CG_Repo"

# Dummy JSON content
DUMMY_DATA = {
    "user": "testuser",
    "email": "testuser@example.com",
    "active": True
}

# GitHub API URL
GITHUB_API_BASE = "https://api.github.com"
FILE_API_URL = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

def encode_content(data: dict) -> str:
    json_str = json.dumps(data, indent=4)
    return base64.b64encode(json_str.encode()).decode()

def get_existing_file_sha():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {"ref": BRANCH}
    response = requests.get(FILE_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["sha"]  # File exists, return SHA for update
    elif response.status_code == 404:
        return None  # File does not exist
    else:
        print(f"❌ Failed to check existing file: {response.status_code}")
        print(response.text)
        return None

def push_file():
    if not GITHUB_TOKEN:
        raise EnvironmentError("GITHUB_TOKEN is not set in environment.")

    sha = get_existing_file_sha()
    content = encode_content(DUMMY_DATA)

    payload = {
        "message": COMMIT_MESSAGE,
        "content": content,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha  # Required if updating an existing file

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.put(FILE_API_URL, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print("✅ JSON file pushed successfully to sathishdummy-repo.")
    else:
        print(f"❌ Failed to push file: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    push_file()
