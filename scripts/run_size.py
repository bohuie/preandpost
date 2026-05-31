"""
Runs Size metric extraction on cloned repositories.

Repository folder structure:
data/
└── repos/
    ├── <REPO_OWNER_1>/
    │   ├── <REPO_NAME_1>/
    │   └── <REPO_NAME_2>/
    └── <REPO_OWNER_2>/
        └── <REPO_NAME_3>/

Example:
data/
└── repos/
    ├── COSC-499-W2023/
    │   └── year-long-project-team-15/
    └── COSC-499-W2025/
        └── capstone-project-team-15/

Output folder structure:
data/
└── outputs/
    └── size/
        ├── files_summary.csv    # File-level metrics
        └── repos_summary.csv    # Repository-level metrics
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv
import sys
import traceback

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

# Import size metric functions
from src.metrics.size import (
    analyze_repository,
    repository_metrics_to_dict,
    file_metrics_to_dict,
)


def save_csv(rows: list[dict], output_path: Path, first_columns: list[str] | None = None) -> None:
    if not rows:
        print(f"No rows to save for {output_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_columns = list(rows[0].keys())

    if first_columns:
        remaining_columns = [col for col in all_columns if col not in first_columns]
        fieldnames = first_columns + remaining_columns
    else:
        fieldnames = all_columns

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_size_metrics_for_repo(
    repo_owner: str,
    repo_name: str,
    repos_base_dir: str | Path,
) -> dict:
    """Run Size metrics for one cloned repository."""

    repo_path = Path(repos_base_dir) / repo_owner / repo_name

    result = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "repo_path": str(repo_path),
        "status": "pending",
        "errors": [],
        "summary": None,
        "files": [],
    }

    if not repo_path.exists():
        result["status"] = "failed"
        result["errors"].append(f"Repository path does not exist: {repo_path}")
        return result

    try:
        repo_metrics, file_metrics = analyze_repository(repo_path)

        summary = repository_metrics_to_dict(repo_metrics)
        summary["repo_owner"] = repo_owner
        summary["repo_name"] = repo_name
        summary["repo_path"] = str(repo_path)

        file_rows = []
        for item in file_metrics:
            row = file_metrics_to_dict(item)
            row["repo_owner"] = repo_owner
            row["repo_name"] = repo_name
            row["repo_path"] = str(repo_path)
            file_rows.append(row)

        result["status"] = "success"
        result["summary"] = summary
        result["files"] = file_rows

        return result

    except Exception as error:
        result["status"] = "failed"
        result["errors"].append(str(error))
        return result


if __name__ == "__main__":

    # ==================== CONFIGURATION ====================

    REPOSITORIES = [
        {
            "repo_owner": "COSC-499-W2023",
            "repo_name": "year-long-project-team-15",
        },
        {
            "repo_owner": "COSC-499-W2025",
            "repo_name": "capstone-project-team-15",
        },
    ]

    REPOS_BASE_DIR = "./data/repos"
    OUTPUT_DIR = "./data/outputs/size"

    SAVE_SUMMARY_CSV = True
    SAVE_FILE_LEVEL_CSV = True

    # ==================== EXECUTION ====================

    print("\n" + "=" * 80)
    print("SIZE METRICS EXTRACTION")
    print("=" * 80)
    print(f"Working directory: {Path.cwd()}")
    print(f"Script location: {Path(__file__).parent}")
    print(f"Repositories base directory: {REPOS_BASE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total repositories to process: {len(REPOSITORIES)}")
    print("=" * 80)

    all_results = []
    summary_rows = []
    file_rows = []
    failed_repos = []

    try:
        for idx, repo_config in enumerate(REPOSITORIES, 1):
            repo_owner = repo_config["repo_owner"]
            repo_name = repo_config["repo_name"]

            print(f"\n[{idx}/{len(REPOSITORIES)}] Processing: {repo_owner}/{repo_name}")

            try:
                result = run_size_metrics_for_repo(
                    repo_owner=repo_owner,
                    repo_name=repo_name,
                    repos_base_dir=REPOS_BASE_DIR,
                )

                all_results.append(result)

                if result["status"] == "success":
                    summary_rows.append(result["summary"])
                    file_rows.extend(result["files"])

                    print("  Status: success")
                    print(f"  Files analyzed: {result['summary']['files']}")
                    print(f"  Lines: {result['summary']['lines']}")
                    print(f"  ncloc: {result['summary']['ncloc']}")
                    print(f"  Comment lines: {result['summary']['comment_lines']}")
                    print(f"  Comment density: {result['summary']['comment_density']}%")
                    print(f"  Statements: {result['summary']['statements']}")
                    print(f"  Functions: {result['summary']['functions']}")
                    print(f"  Classes: {result['summary']['classes']}")

                else:
                    failed_repos.append((repo_owner, repo_name, result["errors"]))
                    print("  Status: failed")
                    for error in result["errors"]:
                        print(f"  Error: {error}")

            except Exception as error:
                print(f"[ERROR] Failed to process {repo_owner}/{repo_name}: {error}")
                failed_repos.append((repo_owner, repo_name, [str(error)]))
                traceback.print_exc()

        # ==================== SAVE OUTPUTS ====================

        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        first_columns = ["repo_owner", "repo_name", "repo_path"]

        if SAVE_SUMMARY_CSV:
            summary_output = output_dir / "repos_summary.csv"
            save_csv(summary_rows, summary_output, first_columns=first_columns)
            print(f"\nSaved repository-level summary to: {summary_output}")

        if SAVE_FILE_LEVEL_CSV:
            file_output = output_dir / "files_summary.csv"
            save_csv(file_rows, file_output, first_columns=first_columns)
            print(f"Saved file-level metrics to: {file_output}")

        # ==================== SUMMARY ====================

        print("\n" + "=" * 80)
        print("SIZE METRICS SUMMARY")
        print("=" * 80)
        print(f"Total repositories processed: {len(all_results)}")
        print(f"Successful: {len([r for r in all_results if r['status'] == 'success'])}")
        print(f"Failed: {len(failed_repos)}")

        if failed_repos:
            print("\n❌ FAILED REPOSITORIES:")
            for repo_owner, repo_name, errors in failed_repos:
                print(f"\n  {repo_owner}/{repo_name}:")
                for error in errors:
                    print(f"    - {error}")

            sys.exit(1)

        print("\n✅ ALL REPOSITORIES SUCCESSFULLY ANALYZED")
        print("=" * 80)

    except Exception as error:
        print(f"\n[FATAL ERROR] {error}")
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 80)
    print(f"✅ SUCCESS - Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)