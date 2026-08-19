"""
We want to validate: Does the data in JSON contain all the data we need to understand the repo?
1. Repo metadata : Do we have all repo metadata fields needed for analysis?

To understand where the repo comes from, what its condition is, and how to read its data.
repo name, owner, default branch, private/public, created_at, updated_at, pushed_at, description, language, repo size

2. branches: Does this json have the branches data we need to understand all the repo workflows?
branch name, branch commit, protected branch

3. commits: Does this json have enough commit data to understand the repo's change history?

4. pull requests: Does this json have enough PR data to understand pr activity?

5. file contents: Does this json store the required file contents/source code?

"""
import json

METADATA_KEYS = {"name", "owner", "full_name", "default_branch", "private", "created_at", "updated_at", "pushed_at",
"description", "language", "size",}

BRANCHES_KEYS = {"name", "commit", "protected"}

COMMIT_KEYS = {"sha", "commit", "stats", "files"}
COMMIT_INNER_KEYS = {"message", "author", "tree"}
# tree sha: To access the repo file/folder snapshot at that commit. 
# It shows which version of the repo structure belongs to this commit
AUTHOR_KEYS = {"name", "email", "date"}
STATS_KEYS = {"total", "additions", "deletions"}
CHANGED_FILE_KEYS = {"filename", "status", "additions", "deletions", "changes"}

PR_KEYS = {"details", "commits", "files", "issue_comments", "review_comments", "reviews",}
PR_DETAILS_KEYS = {"number", "title", "state", "created_at", "user", "head", "base",}
PR_FILE_KEYS = {"filename", "status", "additions", "deletions", "changes",}
PR_COMMIT_KEYS = {"sha","commit",}

FILE_KEYS = {"content"}
SNAPSHOT_KEYS = {"commit_sha", "files"} # Save a reference to the content file
SNAPSHOT_FILE_KEYS = {"file_path", "extension", "file_version_id"}


def validate_metadata(file_path: str):
    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    # Check whether metadata exists
    if "metadata" not in repo_data:
        print("Metadata is missing")
        return None
    
    metadata = repo_data["metadata"]

    # Take all keys in metadata, then convert them into a set
    current_metadata_keys = set(metadata.keys())
    missing_metadata_keys = METADATA_KEYS - current_metadata_keys   # A - B : take items that are in A, but not in B

    if missing_metadata_keys:
        print(f"Metadata is incomplete. Missing keys: {missing_metadata_keys}")
    else:
        print("Metadata validation finished.")

    return repo_data


def validate_branches(repo_data):
    if "branches" not in repo_data:
        print(f"Branches is missing.")
        return
    
    branches = repo_data["branches"]

    # Validate each branch one by one
    for branch in branches:

        current_branches_keys = set(branch.keys())
        missing_branches_keys = BRANCHES_KEYS - current_branches_keys

        if missing_branches_keys:
            print(f"Branches {branch} is incomplete. Missing keys: {missing_branches_keys}")

    print("Branches validation finished.")


def validate_commits(repo_data):
    if "commits" not in repo_data:
        print("Commits is missing.")
        return
    
    commits = repo_data["commits"]

    for commit in commits:

        current_commit_keys = set(commit.keys())
        missing_commit_keys = COMMIT_KEYS - current_commit_keys

        if missing_commit_keys:
            print(f"Commits {commit} is incomplete. Missing keys: {missing_commit_keys}")

        # Check inner commit object: "message", "author", "tree"
        if "commit" in commit:
            commit_info = commit['commit']

            current_inner_keys = set(commit_info.keys())
            missing_inner_keys = COMMIT_INNER_KEYS - current_inner_keys

            if missing_inner_keys:
                print(f"Commits {commit}.commit is incomplete. Missing keys: {missing_inner_keys}")

            # Check author info
            if "author" in commit_info:
                author = commit_info["author"]

                current_author_keys = set(author.keys())
                missing_author_keys = AUTHOR_KEYS - current_author_keys

                if missing_author_keys:
                    print(f"Commits {commit}.author is incomplete. Missing keys: {missing_author_keys}")
            
            if "tree" in commit_info:
                tree = commit_info["tree"]
                if "sha" not in tree:
                    print(f"Commits {commit}.commit.tree.sha is missing")

        # Check total stats
        if "stats" in commit:
            stats = commit["stats"]

            current_stats_keys = set(stats.keys())
            missing_stats_keys = STATS_KEYS - current_stats_keys

            if missing_stats_keys:
                print(f"Commits {commit}.stats is incomplete. Missing keys: {missing_stats_keys}")

        # Check changed files
        if "files" in commit:
            changed_files = commit["files"]

            for changed_file in changed_files:
                current_file_keys = set(changed_file.keys())
                missing_file_keys = CHANGED_FILE_KEYS - current_file_keys

                if missing_file_keys:
                    print(f"Commits {commit}.files is incomplete. Missing keys: {missing_file_keys}")

    print("Commits validation finished.")


def validate_pr(repo_data):
    if "pull_requests" not in repo_data:
        print(f"Pull requests is missing")
        return
    
    pull_requests = repo_data["pull_requests"]

    for pull_request in pull_requests:
        current_pr_keys = set(pull_request.keys())
        missing_pr_keys = PR_KEYS - current_pr_keys

        if missing_pr_keys:
            print(f"Pull request is incomplete. Missing keys: {missing_pr_keys}")

        # Check PR details
        if "details" in pull_request:
            details = pull_request["details"]

            current_details_keys = set(details.keys())
            missing_details_keys = PR_DETAILS_KEYS - current_details_keys

            if missing_details_keys:
                print(f"Pull request details is incomplete. Missing keys: {missing_details_keys}")

        # Check PR commits
        if "commits" in pull_request:
            pr_commits = pull_request["commits"]

            for pr_commit in pr_commits:
                current_commit_keys = set(pr_commit.keys())
                missing_commit_keys = PR_COMMIT_KEYS - current_commit_keys

                if missing_commit_keys:
                    print(f"Pull request commit is incomplete. Missing keys: {missing_commit_keys}")

        # Check PR changed files
        if "files" in pull_request:
            pr_files = pull_request["files"]

            for pr_file in pr_files:
                current_file_keys = set(pr_file.keys())
                missing_file_keys = PR_FILE_KEYS - current_file_keys

                if missing_file_keys:
                    print(f"Pull request file is incomplete. Missing keys: {missing_file_keys}")

    print("Pull requests validation finished.")


def validate_file_contents(repo_data):
    if "file_versions" not in repo_data:
        print("File version is missing")
        return
    
    if "snapshots" not in repo_data:
        print("Snapshots is missing")
        return
    
    file_versions = repo_data["file_versions"]
    snapshots = repo_data["snapshots"]

    # Check every file version has content
    for file_version_id, file_data in file_versions.items():
        current_file_version_keys = set(file_data.keys())
        missing_file_version_keys = FILE_KEYS - current_file_version_keys

        if missing_file_version_keys:
            print(f"File version {file_version_id} is incomplete. Missing keys: {missing_file_version_keys}")

    # Check every snapshot file points to an existing file version
    for snapshot in snapshots:
        current_snapshot_keys = set(snapshot.keys())
        missing_snapshot_keys = SNAPSHOT_KEYS - current_snapshot_keys

        if missing_snapshot_keys:
            print(f"Snapshot is incomplete. Missing keys: {missing_snapshot_keys}")

        files = snapshot["files"]

        for file in files:
            current_snapshot_file_keys = set(file.keys())
            missing_snapshot_file_keys = SNAPSHOT_FILE_KEYS - current_snapshot_file_keys

            if missing_snapshot_file_keys:
                print(f"Snapshot file is incomplete. Missing keys: {missing_snapshot_file_keys}")

    print("File contents validation finished.")



# CONFIGURATION
path_file = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-11-indoor-wayfinding-indoor-wayfinding.json"
# "data/UBCO-COSC499-Winter-2018-Term-1-2/project-12-bus-advisory-offline-real-time-bus-location-tracker.json"
# "data/COSC-499-W2023/year-long-project-team-15.json"
data_valid = validate_metadata(path_file)

if data_valid is not None:
    validate_branches(data_valid)
    validate_commits(data_valid)
    validate_pr(data_valid)
    validate_file_contents(data_valid)

print("\n Validation: Finished")


# Run:  python -m src.validate_json