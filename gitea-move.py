# from gitea import *
from gitea import Gitea, User
import requests
import json
import gitea

# GITEA_USER
# GITEA_TOKEN
# GITEA_DOMAIN
# GITEA_REPO_OWNER
OLD_TOKEN = "c67707bd4abb97d3af6c294f112ee75e0af23ecb"
# SNIPER_TOKEN="f4567fda2c8353576839aa57f935fe060c0bba97"
NEW_TOKEN = "f026cd4e8c45ec093fced16a1a92d6ded85086c2"

gitea_old = Gitea("https://oldgit.spy.rafael.ovh", OLD_TOKEN)
gitea_new = Gitea("https://git.spy.rafael.ovh", NEW_TOKEN)


print("Gitea Version" + gitea_old.get_version())


# def migrate(repo):
#   global OLD_TOKEN
#   params = {
#       # "auth_password": "string",
#       "auth_token": OLD_TOKEN,
#       "auth_username": "rg",
#       "clone_addr": repo.clone_url,
#       # "description": "string",
#       "issues": True,
#       "labels": True,
#       "lfs": False,
#       # "lfs_endpoint": "string",
#       "milestones": True,
#       "mirror": False,
#       # "mirror_interval": "string",
#       "private": True,
#       "pull_requests": True,
#       "releases": True,
#       "repo_name": repo.name,
#       "repo_owner": "rg",
#       "service": "gitea",
#       "uid": 0,
#       "wiki": True
#   }
#   r = requests.post()


def create_migration(username, repo):

    url = f"{gitea_new.url}/api/v1/repos/migrate"
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    params = {
        # "auth_password": "string",
        "auth_token": OLD_TOKEN,
        # "auth_username": "rg",
        "clone_addr": repo.clone_url,
        # "description": "string",
        "issues": True,
        "labels": True,
        "lfs": False,
        # "lfs_endpoint": "string",
        "milestones": True,
        "mirror": False,
        # "mirror_interval": "string",
        "private": True,
        "pull_requests": True,
        "releases": True,
        "repo_name": repo.name,
        "repo_owner": username,
        "service": "gitea",
        "uid": 1,  # "deprecated (only for backwards compatibility"
        "wiki": True,
    }
    auth = ("rg", NEW_TOKEN)

    print(params)
    response = requests.post(url, headers=headers, data=json.dumps(params), auth=auth)

    print(response.status_code)
    if response.status_code != 200:
        print(response.json())


# def migrate_user_repos(username, old_instance, new_instance):
#     old_user = User.request(old_instance, username)
#     new_user = User.request(new_instance, username)

#     repos = gitea_user.get_repositories()
#     for repo in repos:
#         print(f"Migrating {repo}...")
#         try:
#             Repository.request(new_instance, username, repo.name)
#         except gitea.exceptions.NotFoundException:
#             migrate_repo(username, repo)


def migrate_org(owner, org, old_inst, new_inst):
    print(f"Migrating org '{org.name}'...")
    owner = User.request(new_inst, "rg")
    try:
        new_inst.create_org(owner, org.name, org.description, org.location, org.website, org.full_name)
    except gitea.exceptions.AlreadyExistsException:
        print(f"Organization {org.name} already exists. Skip create.")
    for repo in org.get_repositories():
        if repo.mirror:
            print(f"[{org.name}] Repo {repo.name} is mirror - skipping.")
            continue
        print(f"[{org.name}] Migrating {repo.name}...")
        create_migration(org.name, repo)


def main():
    global repos
    u = User.request(gitea_old, "rg")
    repos = u.get_repositories()
    # a(repos[0])
    for repo in repos:
        print(repo.name)
        create_migration("rg", repo)
