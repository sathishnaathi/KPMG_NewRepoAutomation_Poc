import os
import base64
import requests

#GitHub credentials and configuration
GITHUB_TOKEN = os.getenv("REPO_TOKEN")          # Updated token environment variable
GITHUB_USERNAME = os.getenv("REPO_USER")        # Updated username environment variable
REPO_NAME = "kpmg-us-nexus-dummy-sapi"
FEATURE_BRANCH = "Feature/CICDAutomation"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Create repository
def create_repository():
    url = "https://api.github.com/user/repos"
    data = {
        "name": REPO_NAME,
        "private": False,
        "auto_init": False
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    print("Repository created successfully.")
  
#add Readme file
def add_readme():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/README.md"
    content = base64.b64encode(b"# Hello Devsecops team welcome to the repository").decode("utf-8")
    data = {
        "message": "Add README.md",
        "content": content,
        "branch": "main"
    }
    response = requests.put(url, json=data, headers=HEADERS)
    response.raise_for_status()
    print("README.md added successfully.")

def get_main_branch_sha():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/git/ref/heads/main"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["object"]["sha"]
  
#Create feature branch  
def create_feature_branch():
    sha = get_main_branch_sha()
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/git/refs"
    data = {
        "ref": f"refs/heads/{FEATURE_BRANCH}",
        "sha": sha
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    print(f"Feature branch '{FEATURE_BRANCH}' created successfully.")
  
#enable branch protection rule
def enable_branch_protection(branch):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/branches/{branch}/protection"
    data = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1
        },
        "restrictions": None
    }
    response = requests.put(url, json=data, headers=HEADERS)
    response.raise_for_status()
    print(f"Branch protection enabled for '{branch}'.")

def main():
    create_repository()
    add_readme()
    create_feature_branch()
    enable_branch_protection("main")
    enable_branch_protection(FEATURE_BRANCH)

if __name__ == "__main__":
    main()
