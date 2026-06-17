import base64
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from src.file_filter import SKIP_FOLDER, should_include_file


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("Please add GITHUB_TOKEN to the .env file.")

class GithubClient:
    """Fetch reusable raw repository data from GitHub."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self.s = requests.Session()

        self.s.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {token}",
            }
        )

        # Avoid reading the same tree repeatedly.
        self.tree_cache = {}

    def _base(self, owner: str, repo: str) -> str:
        """Build the base API URL for one repository."""
        return f"{self.BASE_URL}/repos/{owner}/{repo}"

    def _get(
        self,
        url: str,
        params: dict | None = None,
        max_retries: int = 5,
    ):
        for attempt in range(max_retries):
            response = self.s.get(
                url,
                params=params,
                timeout=60,
            )

            if response.status_code in {502, 503, 504}:
                wait_time = 5 * (attempt + 1)

                print(
                    f"GitHub server error {response.status_code}. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()

            if not response.text.strip():
                return {}

            return response.json()

        response.raise_for_status()



    def _get_all_pages(
        self,
        url: str,
        params: dict | None = None,
    ) -> list[dict]:
        """Fetch every page from a paginated endpoint."""
        results = []
        page = 1

        while True:
            query = {
                **(params or {}),
                "per_page": 100,
                "page": page,
            }

            batch = self._get(
                url,
                params=query,
            )

            if not batch:
                break

            results.extend(batch)

            if len(batch) < 100:
                break

            page += 1

        return results



    def _fetch_tree_refs(
        self,
        base: str,
        tree_sha: str,
        parent_path: str = "",
    ) -> list[dict]:
        """Collect filtered file references from one tree."""
        cache_key = (tree_sha, parent_path)

        if cache_key in self.tree_cache:
            return self.tree_cache[cache_key]

        tree = self._get(
            f"{base}/git/trees/{tree_sha}"
        )

        files = []

        for item in tree.get("tree", []):
            item_path = (
                f"{parent_path}/{item['path']}"
                if parent_path
                else item["path"]
            )

            if item["type"] == "tree":
                if item["path"].lower() in SKIP_FOLDER:
                    continue

                files.extend(
                    self._fetch_tree_refs(
                        base=base,
                        tree_sha=item["sha"],
                        parent_path=item_path,
                    )
                )

            elif (
                item["type"] == "blob"
                and should_include_file(item_path)
            ):
                files.append(
                    {
                        "file_path": item_path,
                        "extension": Path(item_path).suffix.lower(),
                        "file_version_id": item["sha"],
                    }
                )

        self.tree_cache[cache_key] = files

        return files

    def _fetch_file_versions(
        self,
        base: str,
        version_ids: set[str],
        workers: int = 5,
    ) -> dict[str, dict]:
        """Fetch each unique full file content only once."""

        def fetch_one(version_id: str) -> tuple[str, dict]:
            blob = self._get(
                f"{base}/git/blobs/{version_id}"
            )

            content = base64.b64decode(
                blob.get("content", "")
            ).decode(
                "utf-8",
                errors="replace",
            )

            return version_id, {
                "content": content,
            }

        versions = {}

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(fetch_one, version_id)
                for version_id in version_ids
            ]

            for future in as_completed(futures):
                version_id, data = future.result()
                versions[version_id] = data

        return versions

    def fetch_branches(self, base: str) -> list[dict]:
        """Fetch every repository branch."""
        return self._get_all_pages(
            f"{base}/branches"
        )

    def fetch_tags(self, base: str) -> list[dict]:
        """Fetch every repository tag."""
        return self._get_all_pages(
            f"{base}/tags"
        )

    def fetch_commits(
        self,
        base: str,
        branches: list[dict],
    ) -> list[dict]:
        """Fetch unique commit details from every branch."""
        summaries_by_sha = {}

        for branch in branches:
            summaries = self._get_all_pages(
                f"{base}/commits",
                params={"sha": branch["name"]},
            )

            for summary in summaries:
                summaries_by_sha[summary["sha"]] = summary

        commits = []

        for index, sha in enumerate(summaries_by_sha, start=1):
            print(
                f"Fetching commit {index}/{len(summaries_by_sha)}: "
                f"{sha[:7]}"
            )

            commits.append(
                self._get(
                    f"{base}/commits/{sha}"
                )
            )

        return commits

    def fetch_snapshots(
        self,
        base: str,
        commits: list[dict],
    ) -> tuple[list[dict], dict[str, dict]]:
        """Fetch file references per commit and unique file contents."""
        snapshots = []
        version_ids = set()

        for index, commit in enumerate(commits, start=1):
            sha = commit["sha"]

            print(
                f"Fetching snapshot {index}/{len(commits)}: "
                f"{sha[:7]}"
            )

            files = self._fetch_tree_refs(
                base=base,
                tree_sha=commit["commit"]["tree"]["sha"],
            )

            snapshots.append(
                {
                    "commit_sha": sha,
                    "files": files,
                }
            )

            version_ids.update(
                file["file_version_id"]
                for file in files
            )

        print(
            f"Fetching {len(version_ids)} unique file versions..."
        )

        file_versions = self._fetch_file_versions(
            base=base,
            version_ids=version_ids,
        )

        return snapshots, file_versions

    def fetch_pull_requests(self, base: str) -> list[dict]:
        """Fetch detailed PR data, including comments and reviews."""
        summaries = self._get_all_pages(
            f"{base}/pulls",
            params={"state": "all"},
        )

        pull_requests = []

        for index, summary in enumerate(summaries, start=1):
            number = summary["number"]

            print(
                f"Fetching PR {index}/{len(summaries)}: "
                f"#{number}"
            )

            pull_requests.append(
                {
                    "details": self._get(
                        f"{base}/pulls/{number}"
                    ),
                    "commits": self._get_all_pages(
                        f"{base}/pulls/{number}/commits"
                    ),
                    "files": self._get_all_pages(
                        f"{base}/pulls/{number}/files"
                    ),
                    "issue_comments": self._get_all_pages(
                        f"{base}/issues/{number}/comments"
                    ),
                    "review_comments": self._get_all_pages(
                        f"{base}/pulls/{number}/comments"
                    ),
                    "reviews": self._get_all_pages(
                        f"{base}/pulls/{number}/reviews"
                    ),
                }
            )

        return pull_requests

    def fetch_full(
        self,
        owner: str,
        repo: str,
    ) -> dict:
        """Fetch one reusable raw repository report."""
        base = self._base(owner, repo)

        metadata = self._get(base)
        branches = self.fetch_branches(base)
        tags = self.fetch_tags(base)
        commits = self.fetch_commits(base, branches)

        snapshots, file_versions = self.fetch_snapshots(
            base=base,
            commits=commits,
        )

        pull_requests = self.fetch_pull_requests(base)

        return {
            "owner": owner,
            "repository": repo,
            "metadata": metadata,
            "branches": branches,
            "tags": tags,
            "commits": commits,
            "snapshots": snapshots,
            "file_versions": file_versions,
            "pull_requests": pull_requests,
            "manifest": {
                "branch_count": len(branches),
                "tag_count": len(tags),
                "commit_count": len(commits),
                "snapshot_count": len(snapshots),
                "unique_file_version_count": len(file_versions),
                "pull_request_count": len(pull_requests),
            },
            "fetched_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

    def save_repository_json(
        self,
        repository_data: dict,
    ) -> str:
        """Save one report to data/{owner}/{repository}.json."""
        output_directory = os.path.join(
            "data",
            repository_data["owner"],
        )

        os.makedirs(
            output_directory,
            exist_ok=True,
        )

        output_path = os.path.join(
            output_directory,
            f"{repository_data['repository']}.json",
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                repository_data,
                file,
                indent=2,
                ensure_ascii=False,
            )

        return os.path.abspath(output_path)