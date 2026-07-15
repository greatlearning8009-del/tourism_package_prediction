# Hosting script: push all project files to the GitHub repo using PyGithub.
# A GitHub Codespace launched from this repo then builds and runs the containers,
# and the pushed workflow file triggers the GitHub Actions pipeline.
import os
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "greatlearning8009-del/Tourism_Package_Prediction"   # <owner>/<repo>

g = Github(GITHUB_TOKEN)
user = g.get_user()

# Create the repo if it does not exist yet, otherwise reuse it
try:
    repo = g.get_repo(REPO_NAME)
    print(f"Using existing repo: {repo.html_url}")
except Exception:
    repo = user.create_repo(REPO_NAME.split("/")[-1], private=False, auto_init=True)
    print(f"Created repo: {repo.html_url}")

# repo_path == local_path for each file. The workflow file is LAST so the
# pipeline triggers once, after every other file is already in the repo.
files = [
    "tourism_project/requirements.txt",
    "tourism_project/model_building/data_register.py",
    "tourism_project/model_building/prep.py",
    "tourism_project/model_building/train.py",
    "tourism_project/deployment/backend/app.py",
    "tourism_project/deployment/backend/requirements.txt",
    "tourism_project/deployment/backend/Dockerfile",
    "tourism_project/deployment/frontend/app.py",
    "tourism_project/deployment/frontend/requirements.txt",
    "tourism_project/deployment/frontend/Dockerfile",
    "tourism_project/hosting/hosting.py",
    ".github/workflows/pipeline.yml",
]


def upsert(path):
    with open(path, "rb") as f:
        content = f.read()
    try:
        existing = repo.get_contents(path, ref="main")
        repo.update_file(path, f"Update {path}", content, existing.sha, branch="main")
        print(f"Updated: {path}")
    except Exception:
        repo.create_file(path, f"Add {path}", content, branch="main")
        print(f"Created: {path}")


for p in files:
    upsert(p)

print("All files pushed. GitHub Actions runs the pipeline on the workflow commit.")
