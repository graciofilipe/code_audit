import os
from gemini_bits import generate
from github_to_text import repo_to_bucket

BUCKET_NAME = os.getenv("BUCKET_NAME")
PROJECT_ID = os.getenv("PROJECT_ID")


def repo_to_analysis(
    repo_url, repo_sub_path, bucket_name, path_to_design_document=None
):

    repo_to_bucket(
        repo_url=repo_url, bucket_name=bucket_name, repo_sub_path=repo_sub_path
    )

    # sleep for 3 seconds:
    import time

    time.sleep(3)

    generate(
        path_to_code=f"gs://{BUCKET_NAME}/" + repo_url.split("/")[-1] + repo_sub_path.replace("/", "_") + ".txt",
        path_to_design_document=None,
    )


if __name__ == "__main__":

    repo_to_analysis(
        repo_url="https://github.com/GoogleCloudPlatform/guacamole-on-gcp",
        repo_sub_path="",
        bucket_name=BUCKET_NAME,
    )
