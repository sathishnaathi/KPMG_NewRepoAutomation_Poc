import os
import base64
import requests

#GitHub credentials and configuration
GITHUB_TOKEN = os.getenv("REPO_TOKEN")          # Updated token environment variable
GITHUB_USERNAME = os.getenv("REPO_USER")        # Updated username environment variable
REPO_NAME = "DummySathish_Repo"
FEATURE_BRANCH = "Feature/CICDAutomation"
ENVIRONMENT_NAME = "UAT-PROD"

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

# def enable_branch_protection_pattern(branch_pattern):
#     url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/branches/{branch_pattern}/protection"
#     data = {
#         "required_status_checks": {
#             "strict": True,
#             "contexts": []
#         },
#         "enforce_admins": True,
#         "required_pull_request_reviews": {
#             "required_approving_review_count": 1
#         },
#         "restrictions": None
#     }
#     response = requests.put(url, json=data, headers=HEADERS)
#     if response.status_code == 200:
#         print(f"Branch protection enabled for pattern '{branch_pattern}'.")
#     else:
#         print(f"Failed to enable branch protection for pattern '{branch_pattern}': {response.status_code}")
#         print(response.json())

# Create environment UAT-PROD
def create_environment():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/environments/{ENVIRONMENT_NAME}"
    response = requests.put(url, headers=HEADERS)
    if response.status_code in (200,201, 204):
        print(f"Environment '{ENVIRONMENT_NAME}' created successfully.")
    else:
        print(f"Failed to create environment '{ENVIRONMENT_NAME}': {response.status_code}")
        print(response.json())
        
# def add_deployment_protection_rules():
#     url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/environments/{ENVIRONMENT_NAME}/deployment_protection_rules"
#     data = {
#         "name": "required_reviewers",
#         "type": "required_reviewers",
#         "prevent_self_review": True
#     }
#     response = requests.post(url, headers=HEADERS, json=data)
#     if response.status_code == 201:
#         print("Deployment protection rules set successfully.")
#     else:
#         print(f"Failed to set deployment protection rules: {response.status_code}")
#         print(response.json())

# def set_deployment_branches_and_tags():
#     url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/environments/{ENVIRONMENT_NAME}/deployment_branch_policies"
#     data = {
#         "protected_branches": True,  
#         "custom_branch_policies": []  
#     }
#     response = requests.put(url, json=data, headers=HEADERS)
#     if response.status_code in (200, 201, 204):
#         print("Deployment branches and tags configured successfully (none allowed).")
#     else:
#         print(f"Failed to configure deployment branches and tags: {response.status_code}")
#         print(response.json())

def main():
    create_repository()
    add_readme()
    create_feature_branch()
    enable_branch_protection("main")
    enable_branch_protection(FEATURE_BRANCH)
    
    # branch_patterns = ["release", "uatdeploy", "proddeploy"]  # You can also try ["release*", "uatdeploy*", "proddeploy*"] if needed
    # for pattern in branch_patterns:
    # enable_branch_protection_pattern(pattern)
    create_environment()
    

if __name__ == "__main__":
    main()
