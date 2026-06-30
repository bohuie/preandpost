from src.file_filter import should_include_file


def extract_files(repo_data: dict) -> list[dict]:
    """
    Extract filtered file contents from the latest commit
    on the repository's default branch.
    """

    # 1. Get the default branch name.
    default_branch_name = (
        repo_data["metadata"]["default_branch"]
    )

    # 2. Find the latest commit SHA on the default branch.
    latest_sha = None

    for branch in repo_data["branches"]:
        if branch["name"] == default_branch_name:
            latest_sha = branch["commit"]["sha"]
            break

    if latest_sha is None:
        raise ValueError(
            "Could not find the latest commit SHA for "
            f"default branch {default_branch_name!r}."
        )

    # 3. Find the snapshot belonging to that commit.
    latest_snapshot = None

    for snapshot in repo_data["snapshots"]:
        if snapshot["commit_sha"] == latest_sha:
            latest_snapshot = snapshot
            break

    if latest_snapshot is None:
        raise ValueError(
            "Could not find a snapshot for commit "
            f"{latest_sha!r}."
        )

    # 4. Read file contents from the file-version dictionary.
    file_versions = repo_data["file_versions"]
    result: list[dict] = []

    for file_item in latest_snapshot["files"]:
        file_path = file_item["file_path"]
        version_id = file_item["file_version_id"]

        # JSON object keys are normally strings.
        version_key = str(version_id)

        if version_key in file_versions:
            version_data = file_versions[version_key]
        elif version_id in file_versions:
            version_data = file_versions[version_id]
        else:
            raise KeyError(
                f"File version {version_id!r} was not found "
                f"for {file_path!r}."
            )

        content = version_data.get("content", "")

        # Apply the repository-independent file filter.
        if not should_include_file(
            file_path=file_path,
            content=content,
        ):
            continue

        result.append(
            {
                "path": file_path,
                "extension": file_item.get(
                    "extension",
                    "",
                ),
                "content": content,
            }
        )

    return result

# {} dictionary
# [] list
