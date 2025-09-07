import os
import json
import base64
import requests

# Configuration
GITHUB_TOKEN = os.getenv("REPO_TOKEN")  # GitHub token from environment
REPO_OWNER = os.getenv("REPO_OWNER")    # GitHub username or org
REPO_NAME = "SathishDummy-Repo"
FILE_PATH = "configs/data.json"
BRANCH = "develop"
COMMIT_MESSAGE = "Automated: Add dummy JSON file from KPMG_NewRepoAutomation_Poc"

# Dummy JSON content
DUMMY_DATA = {
    "user": "Sathish",
    "email": "sathishkumar@example.com",
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
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {"ref": BRANCH}
    response = requests.get(FILE_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["sha"]
    elif response.status_code == 404:
        return None
    else:
        print(f"❌ Failed to check existing file: {response.status_code}")
        print(response.text)
        return None

def push_file():
    if not GITHUB_TOKEN or not REPO_OWNER:
        raise EnvironmentError("Missing REPO_TOKEN or REPO_OWNER environment variable.")

    print(f"Pushing to: {FILE_API_URL} on branch {BRANCH}")

    sha = get_existing_file_sha()
    content = encode_content(DUMMY_DATA)

    payload = {
        "message": COMMIT_MESSAGE,
        "content": content,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.put(FILE_API_URL, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print("✅ JSON file pushed successfully.")
    else:
        print(f"❌ Failed to push file: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    push_file()

