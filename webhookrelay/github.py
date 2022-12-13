from cfg import USERNAME, PASSWORD, ENDPOINT
from portainer import Portainer, Stack

client = Portainer(ENDPOINT, USERNAME, PASSWORD)


def get_giturls(repo_data):
    return [
        repo_data["git_url"],
        repo_data["ssh_url"],
        repo_data["clone_url"],
        repo_data["svn_url"]
    ]


def get_stack_list():
    stacks = []
    stack_data = client.get_stacks()
    for i in stack_data:
        if not i.get("AutoUpdate", {}):
            continue
        if not i["AutoUpdate"].get("Webhook"):
            continue
        if not i.get("GitConfig"):
            continue
        gitconfig = i["GitConfig"]
        if not gitconfig.get("URL"):
            continue
        if not gitconfig.get("ReferenceName"):
            continue
        if not gitconfig.get("ConfigFilePath"):
            continue

        stack = Stack(
                i["Name"],
                gitconfig["URL"],
                gitconfig["ConfigFilePath"],
                gitconfig["ReferenceName"],
                i["AutoUpdate"]["Webhook"])
        stacks.append(stack)
    return stacks


def process_webhook(data):
    repo_data = data.get("repository")
    if not repo_data:
        return

    stacks = get_stack_list()
    for i in stacks:
        if i.git_url not in get_giturls(repo_data):
            continue

        if i.git_ref != data["ref"]:
            continue

        updated_files = []
        updated_files.extend(data["head_commit"]["added"])
        updated_files.extend(data["head_commit"]["removed"])
        updated_files.extend(data["head_commit"]["modified"])
        
        if i.git_configfile not in updated_files:
            continue

        commit = data["head_commit"]["id"]
        print(f"commit {commit} triggered webhook for {i.name} {i.webhook}")
        print(i.webhook(i.webhook))
