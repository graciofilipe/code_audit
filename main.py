import os
from gemini_bits import generate
from github_to_text import repo_to_bucket
import argparse

def repo_to_analysis(
    repo_url, repo_sub_path, bucket_name, project_id, model_name
    ):

    print(f"repo_url: {repo_url} - {type(repo_url)}")
    print(f"repo_sub_path: {repo_sub_path} - {type(repo_sub_path)}")
    print(f"bucket_name: {bucket_name} - {type(bucket_name)}")
    print(f"project_id: {project_id} - {type(project_id)}")

    repo_to_bucket(
        repo_url=repo_url, bucket_name=bucket_name, repo_sub_path=repo_sub_path, project_id=project_id
    )

    # sleep for 3 seconds:
    import time
    time.sleep(3)

    generate(
        project_id=project_id,
        bucket_name=bucket_name,
        path_to_code=f"gs://{bucket_name}/" + repo_url.split("/")[-1] + repo_sub_path.replace("/", "_") + ".txt",
        model_name=model_name,
        path_to_design_document=None,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--bucket_name", required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--repo_url", required=True)
    parser.add_argument("--repo_sub_path", required=False, default="")
    
    args = parser.parse_args()

    repo_to_analysis(
        repo_url=args.repo_url,
        repo_sub_path=args.repo_sub_path,
        bucket_name=args.bucket_name,
        project_id=args.project_id,
        model_name=args.model_name,
    )