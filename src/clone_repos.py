"""
Clones one or more GitHub repositories into a structured local directory.

Configuration:
- REPO_OWNER:
  GitHub organization or username that owns the repositories.
  Example:
      REPO_OWNER = "COSC-499-W2025"

- REPO_NAMES:
  List of repository names to clone from the selected owner.
  Example:
      REPO_NAMES = [
          "capstone-project-team-15",
      ]

- OUTPUT_DIR:
  Base folder used to store the cloned repositories.
  Example:
      OUTPUT_DIR = "./data"

- USE_SSH:
  If False, clone repositories using HTTPS.
  If True, clone repositories using SSH.

- UPDATE_IF_EXISTS:
  If False, skip repositories that already exist locally.
  If True, update existing repositories using git pull.

Folder structure:
data/
└── repos/
    └── <REPO_OWNER>/
        ├── <REPO_NAME_1>/
        ├── <REPO_NAME_2>/
        └── ...

Example:
data/
└── repos/
    └── COSC-499-W2025/
        └── capstone-project-team-15/
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import subprocess
import sys
import traceback


def build_clone_url(repo_owner: str, repo_name: str, use_ssh: bool = False) -> str:
    """Build a GitHub clone URL from owner/organization and repository name."""
    if use_ssh:
        return f"git@github.com:{repo_owner}/{repo_name}.git"

    return f"https://github.com/{repo_owner}/{repo_name}.git"


def clone_repository(
    repo_owner: str,
    repo_name: str,
    output_base_dir: str | Path,
    use_ssh: bool = False,
    update_if_exists: bool = False,
) -> dict:
    """
    Clone one repository into data/repos/<repo_owner>/<repo_name>.

    If the repository already exists locally:
    - Skip it by default
    - Or run git pull if update_if_exists=True
    """

    output_base_dir = Path(output_base_dir)
    destination_root = output_base_dir / "repos" / repo_owner
    destination_root.mkdir(parents=True, exist_ok=True)

    destination_path = destination_root / repo_name
    clone_url = build_clone_url(repo_owner, repo_name, use_ssh=use_ssh)

    result = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "clone_url": clone_url,
        "destination_path": str(destination_path),
        "status": "pending",
        "errors": [],
    }

    try:
        if destination_path.exists():
            if update_if_exists:
                print(f"  Repository already exists. Updating with git pull: {destination_path}")

                subprocess.run(
                    ["git", "-C", str(destination_path), "pull"],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                result["status"] = "updated"
                return result

            print(f"  Skipping because repository already exists: {destination_path}")
            result["status"] = "skipped"
            return result

        print(f"  Clone URL: {clone_url}")
        print(f"  Destination: {destination_path}")

        subprocess.run(
            ["git", "clone", clone_url, str(destination_path)],
            check=True,
            capture_output=True,
            text=True,
        )

        result["status"] = "success"
        return result

    except subprocess.CalledProcessError as error:
        error_message = error.stderr.strip() or str(error)
        result["status"] = "failed"
        result["errors"].append(error_message)
        return result

    except Exception as error:
        result["status"] = "failed"
        result["errors"].append(str(error))
        return result


if __name__ == "__main__":

    # ==================== CONFIGURATION ====================

    REPO_OWNER = "COSC-499-W2025"

    REPO_NAMES = [
        "capstone-project-team-15",
    ]

    OUTPUT_DIR = "./data"
    USE_SSH = False
    UPDATE_IF_EXISTS = False

    # ==================== EXECUTION ====================

    print("\n" + "=" * 80)
    print("GITHUB MULTIPLE REPOSITORY CLONING")
    print("=" * 80)
    print(f"Working directory: {Path.cwd()}")
    print(f"Script location: {Path(__file__).parent}")
    print(f"Repository owner: {REPO_OWNER}")
    print(f"Output directory: {Path(OUTPUT_DIR) / 'repos' / REPO_OWNER}")
    print(f"Total repositories to process: {len(REPO_NAMES)}")
    print(f"Use SSH: {USE_SSH}")
    print(f"Update if exists: {UPDATE_IF_EXISTS}")
    print("=" * 80)

    all_results = []
    failed_repos = []

    try:
        for idx, repo_name in enumerate(REPO_NAMES, 1):
            print(f"\n[{idx}/{len(REPO_NAMES)}] Processing: {repo_name}")

            try:
                result = clone_repository(
                    repo_owner=REPO_OWNER,
                    repo_name=repo_name,
                    output_base_dir=OUTPUT_DIR,
                    use_ssh=USE_SSH,
                    update_if_exists=UPDATE_IF_EXISTS,
                )

                all_results.append(result)

                if result["status"] == "failed":
                    failed_repos.append((repo_name, result["errors"]))

                print(f"  Status: {result['status']}")

            except Exception as error:
                print(f"[ERROR] Failed to process {repo_name}: {error}")
                failed_repos.append((repo_name, [str(error)]))
                traceback.print_exc()

        # ==================== SUMMARY ====================

        print("\n" + "=" * 80)
        print("CLONING SUMMARY")
        print("=" * 80)
        print(f"Total repositories processed: {len(all_results)}")
        print(f"Successful clones: {len([r for r in all_results if r['status'] == 'success'])}")
        print(f"Updated: {len([r for r in all_results if r['status'] == 'updated'])}")
        print(f"Skipped: {len([r for r in all_results if r['status'] == 'skipped'])}")
        print(f"Failed: {len(failed_repos)}")

        if failed_repos:
            print("\n❌ FAILED REPOSITORIES:")
            for repo_name, errors in failed_repos:
                print(f"\n  {repo_name}:")
                for error in errors:
                    print(f"    - {error}")

            sys.exit(1)

        print("\n✅ ALL REPOSITORIES PROCESSED WITHOUT FATAL ERRORS")
        print("=" * 80)

    except Exception as error:
        print(f"\n[FATAL ERROR] {error}")
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 80)
    print(f"✅ SUCCESS - Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)