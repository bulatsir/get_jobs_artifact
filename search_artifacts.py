import requests
import json

# Define GitLab credentials and group name
GITLAB_HOST = ""
PRIVATE_TOKEN = ""
GROUP_NAME = ""

# Define the name of the job and artifact to retrieve
JOB_NAME = ""
ARTIFACT_NAME = ""


# Get the id of the group
def get_group_id():
    url = f"{GITLAB_HOST}/api/v4/groups?search={GROUP_NAME}"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    groups = json.loads(response.text)
    group_id = groups[0]["id"]
    print(group_id)
    return group_id


# Get a list of projects in the group
def get_project_ids(group_id):
    url = f"{GITLAB_HOST}/api/v4/groups/{group_id}/projects?pagination=keyset&per_page=50&order_by=id"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    projects = json.loads(response.text)
    project_ids = [project["id"] for project in projects]
    print(project_ids)
    if len(project_ids) > 0:
        return project_ids
    else:
        return None


# Get the ID of the latest job in a project
def get_latest_job_id(project_id):
    url = f"{GITLAB_HOST}/api/v4/projects/{project_id}/jobs"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    params = {"scope": "success", "per_page": 1, "ref": "main", "name": "get_dependents"}
    response = requests.get(url, headers=headers, params=params)
    jobs = json.loads(response.text)
    if len(jobs) > 0:
        return jobs[0]["id"]
    else:
        return None


# Download the specified artifact from a job
def download_artifact(job_id, project_id):
    url = f"{GITLAB_HOST}/api/v4/projects/{project_id}/jobs/{job_id}/artifacts/{ARTIFACT_NAME}"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


group_id = get_group_id()
project_ids = get_project_ids(group_id)

for project in project_ids:
    job_id = get_latest_job_id(project)
    artifacts = []
    if job_id is not None:
        artifact = download_artifact(job_id, project)
        if artifact is not None:
            artifacts.append(artifact)


print(artifacts)