import os
import requests
from github import Github
from google.cloud import storage
from google.cloud import secretmanager

# import environmental variable "PROJECT_ID"
PROJECT_ID = os.getenv("PROJECT_ID")


# get token from GCP secret manager
client = secretmanager.SecretManagerServiceClient()
secret_name = f"projects/{PROJECT_ID}/secrets/github_pat/versions/latest"
response = client.access_secret_version(request={"name": secret_name})
githun_pat = response.payload.data.decode("UTF-8")


def recursive_fetch_files(repo, contents):
    files_data = []
    for content_file in contents:
        if content_file.type == "dir":
            files_data += recursive_fetch_files(
                repo, repo.get_contents(content_file.path)
            )
        else:
            file_content = ""
            file_content += f"\n'''---START OF FILE: {content_file.path} ---\n"

            if content_file.encoding == "base64":
                try:
                    file_content += content_file.decoded_content.decode("utf-8")
                except UnicodeDecodeError:  # catch decoding errors
                    file_content += "[Content not decodable]"
            elif content_file.encoding == "none":
                # Handle files with encoding "none" here
                print(
                    f"Warning: Skipping {content_file.path} due to unsupported encoding 'none'."
                )
                continue
            else:
                # Handle other unexpected encodings here
                print(
                    f"Warning: Skipping {content_file.path} due to unexpected encoding '{content_file.encoding}'."
                )
                continue

            file_content += " ---END OF FILE--- \n \n '''"
            files_data.append(file_content)
    return files_data


def fetch_all_files(repo_url, repo_sub_path=""):
    """Fetch all files from the GitHub repository."""

    # Extract repository owner and name from the URL
    repo_parts = repo_url.split("/")
    owner = repo_parts[-2]
    repo_name = repo_parts[-1]

    # Authenticate with GitHub API (replace with your personal access token)
    g = Github(githun_pat)
    repo = g.get_repo(f"{owner}/{repo_name}")
    contents = repo.get_contents(repo_sub_path)

    files_data = recursive_fetch_files(repo, contents)

    return files_data


def repo_to_bucket(repo_url, bucket_name, repo_sub_path=""):
    repo_name = repo_url.split("/")[-1]

    files_data = fetch_all_files(repo_url, repo_sub_path)

    full_code_string = " ".join(files_data)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(repo_name + repo_sub_path.replace("/", "_") + ".txt")
    blob.upload_from_string(full_code_string)
