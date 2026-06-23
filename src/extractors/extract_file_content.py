# Create function to extract files
def extract_files(repo_data: dict, sonar_data: dict) -> list[dict]:
    # 1. Build set of file paths from sonar components (this is the filter)
    sonar_paths = set()
    for comp in sonar_data["components"]:
        sonar_paths.add(comp["path"])

    # 2. Extract default branch name
    default_branch_name = repo_data["metadata"]["default_branch"]

    # 3. Last commit on default branch
    latest_sha = None
    for branch in repo_data["branches"]:
        if branch["name"] == default_branch_name:
            latest_sha = branch["commit"]["sha"]
            break   # Exit loop once found


    # 4. Snapshot of the commit
    latest_snapshot = None
    for snapshot in repo_data["snapshots"]:
        if snapshot["commit_sha"] == latest_sha:
            latest_snapshot = snapshot
            break   # Exit loop once found


    # 5. Extract file content only for files that exist in sonar list
    file_version = repo_data["file_versions"]
    result = []                                 # list for the results
    for file in latest_snapshot["files"]:

        if file["file_path"] in sonar_paths:
            version_id = file["file_version_id"]

            result.append({     # To store data in a list
                "path": file["file_path"],
                "extension": file["extension"],
                "content": file_version[version_id]["content"],
            })

    return result

# {} dictionary
# [] list
